export enum ClassCheckMode {
  None = "None",
  CheckClass = "Check class",
  CheckClassConstructor = "Check class constructor",
}

const FLAGS: Record<ClassCheckMode, string | null> = {
  [ClassCheckMode.None]: null,
  [ClassCheckMode.CheckClass]: "--check-class",
  [ClassCheckMode.CheckClassConstructor]: "--check-class-constructor",
};

export function classCheckFlag(mode: ClassCheckMode): string | null {
  return FLAGS[mode];
}
