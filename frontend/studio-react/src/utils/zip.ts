import type { CodeFile } from '../types';

let CRC_TABLE: number[] | null = null;

function crc32(str: string): number {
  if (!CRC_TABLE) {
    CRC_TABLE = [];
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      CRC_TABLE[n] = c;
    }
  }
  const bytes = new TextEncoder().encode(str);
  let crc = 0 ^ (-1);
  for (let i = 0; i < bytes.length; i++) crc = (crc >>> 8) ^ CRC_TABLE[(crc ^ bytes[i]) & 0xFF];
  return (crc ^ (-1)) >>> 0;
}

export function zipFiles(files: CodeFile[]): Blob {
  const encoder = new TextEncoder();
  const chunks: Uint8Array[] = [];
  let offset = 0;
  const push = (arr: Uint8Array) => { chunks.push(arr); offset += arr.length; };
  const u16 = (n: number) => new Uint8Array([n & 0xFF, (n >>> 8) & 0xFF]);
  const u32 = (n: number) => new Uint8Array([n & 0xFF, (n >>> 8) & 0xFF, (n >>> 16) & 0xFF, (n >>> 24) & 0xFF]);

  const central: Array<{ nameBytes: Uint8Array; crc: number; size: number; localHeaderOffset: number }> = [];
  files.forEach(file => {
    const nameBytes = encoder.encode(file.name);
    const dataBytes = encoder.encode(file.content);
    const crc = crc32(file.content);
    const size = dataBytes.length;
    const localHeaderOffset = offset;

    push(u32(0x04034b50)); push(u16(20)); push(u16(0)); push(u16(0));
    push(u16(0)); push(u16(0));
    push(u32(crc)); push(u32(size)); push(u32(size));
    push(u16(nameBytes.length)); push(u16(0));
    push(nameBytes); push(dataBytes);

    central.push({ nameBytes, crc, size, localHeaderOffset });
  });

  const centralStart = offset;
  central.forEach(entry => {
    push(u32(0x02014b50)); push(u16(20)); push(u16(20)); push(u16(0)); push(u16(0));
    push(u16(0)); push(u16(0));
    push(u32(entry.crc)); push(u32(entry.size)); push(u32(entry.size));
    push(u16(entry.nameBytes.length)); push(u16(0)); push(u16(0));
    push(u16(0)); push(u16(0)); push(u32(0));
    push(u32(entry.localHeaderOffset));
    push(entry.nameBytes);
  });
  const centralSize = offset - centralStart;

  push(u32(0x06054b50));
  push(u16(0)); push(u16(0));
  push(u16(central.length)); push(u16(central.length));
  push(u32(centralSize)); push(u32(centralStart)); push(u16(0));

  return new Blob(chunks as unknown as BlobPart[], { type: 'application/zip' });
}

export function downloadZip(files: CodeFile[], zipName: string) {
  const blob = zipFiles(files);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = zipName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
