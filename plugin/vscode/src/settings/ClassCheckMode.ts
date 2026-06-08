export enum ClassCheckMode {
  None = "none",
  CheckClass = "checkClass",
  CheckClassConstructor = "checkClassConstructor",
}

const FLAGS: Record<ClassCheckMode, string | null> = {
  [ClassCheckMode.None]: null,
  [ClassCheckMode.CheckClass]: "--check-class",
  [ClassCheckMode.CheckClassConstructor]: "--check-class-constructor",
};

export function classCheckFlag(mode: ClassCheckMode): string | null {
  return FLAGS[mode];
}
