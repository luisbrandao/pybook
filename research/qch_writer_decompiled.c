// FUN_0041b6e1 @ 0041b6e1

void __stdcall FUN_0041b6e1(void)

{
  int *piVar1;
  undefined4 uVar2;
  DWORD DVar3;
  byte bVar4;
  undefined *puVar5;
  int iVar6;
  int unaff_EBP;
  int iVar7;
  int iVar8;
  undefined4 *in_FS_OFFSET;
  
  FUN_00491944((int *)(unaff_EBP + -0x6dc));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6dc));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6dc),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x110c;
  FUN_00491944((int *)(unaff_EBP + -0x6e0));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6e0));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6e0),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x1118;
  FUN_00491944((int *)(unaff_EBP + -0x6e4));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6e4));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6e4),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x1124;
  FUN_00491944((int *)(unaff_EBP + -0x6e8));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6e8));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6e8),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x1130;
  FUN_00491944((int *)(unaff_EBP + -0x6ec));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6ec));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6ec),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x113c;
  FUN_00491944((int *)(unaff_EBP + -0x6f0));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6f0));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6f0),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  bVar4 = 0x80;
  if (*(char *)(*(int *)(unaff_EBP + 8) + 1) == '\0') {
    bVar4 = 0;
  }
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(byte *)(*(int *)(unaff_EBP + 8) + 0x4c) |
               *(char *)(*(int *)(unaff_EBP + 8) + 0x4d) * '\x02' |
               *(char *)(*(int *)(unaff_EBP + 8) + 0x4e) << 2 |
               *(char *)(*(int *)(unaff_EBP + 8) + 0x4f) << 3 |
               *(char *)(*(int *)(unaff_EBP + 8) + 0x50) << 4 | bVar4);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x54));
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x58));
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x5c));
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x85498));
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x85499));
  *(undefined2 *)(unaff_EBP + -0x744) = 0x1148;
  FUN_00491944((int *)(unaff_EBP + -0x6f4));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6f4));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x6f4),2);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
  FUN_0048a5dc((int *)(unaff_EBP + -0x10cc),*(int *)(*(int *)(unaff_EBP + 8) + 0x3c),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x10cc));
  FUN_0048a5dc((int *)(unaff_EBP + -0x10d4),*(int *)(*(int *)(unaff_EBP + 8) + 0x3c),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x10d0));
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0xe58));
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x68));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x68); iVar6 = iVar6 + 1) {
    *(undefined2 *)(unaff_EBP + -0x744) = 0x1154;
    FUN_00491944((int *)(unaff_EBP + -0x6f8));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
    FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6f8));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    FUN_00491a74((int *)(unaff_EBP + -0x6f8),2);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x86c + iVar6 * 4));
    *(undefined2 *)(unaff_EBP + -0x744) = 0;
  }
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x44));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar6 = iVar6 + 1) {
    *(undefined2 *)(unaff_EBP + -0x744) = 0x1160;
    FUN_00491944((int *)(unaff_EBP + -0x6fc));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
    FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x6fc));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    FUN_00491a74((int *)(unaff_EBP + -0x6fc),2);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
    *(undefined2 *)(unaff_EBP + -0x744) = 0;
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar6 = iVar6 + 1) {
    for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0xe58); iVar7 = iVar7 + 1) {
      FUN_0048a5dc((int *)(unaff_EBP + -0x10dc),
                   *(int *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x80 + 0x3e5c + iVar7 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x10dc));
      FUN_0048a5dc((int *)(unaff_EBP + -0x10e4),
                   *(int *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x80 + 0x3e5c + iVar7 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x10e0));
    }
  }
  FUN_0048a5dc((int *)(unaff_EBP + -0x10ec),*(int *)(*(int *)(unaff_EBP + 8) + 0x48),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x10ec));
  FUN_0048a5dc((int *)(unaff_EBP + -0x10f4),*(int *)(*(int *)(unaff_EBP + 8) + 0x48),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x10f0));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x48); iVar6 = iVar6 + 1) {
    *(undefined2 *)(unaff_EBP + -0x744) = 0x116c;
    FUN_00491944((int *)(unaff_EBP + -0x700));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
    FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x700));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    FUN_00491a74((int *)(unaff_EBP + -0x700),2);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
    *(undefined2 *)(unaff_EBP + -0x744) = 0;
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x48); iVar6 = iVar6 + 1) {
    for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0xe58); iVar7 = iVar7 + 1) {
      FUN_0048a5dc((int *)(unaff_EBP + -0x10fc),
                   *(int *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x80 + 0x13e5c + iVar7 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x10fc));
      FUN_0048a5dc((int *)(unaff_EBP + -0x1104),
                   *(int *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x80 + 0x13e5c + iVar7 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x1100));
    }
  }
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0xe04));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0xe04); iVar6 = iVar6 + 1) {
    *(undefined2 *)(unaff_EBP + -0x744) = 0x1178;
    FUN_00491944((int *)(unaff_EBP + -0x704));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
    FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x704));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    FUN_00491a74((int *)(unaff_EBP + -0x704),2);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
    *(undefined2 *)(unaff_EBP + -0x744) = 0;
  }
  FUN_0048a5dc((int *)(unaff_EBP + -0x110c),*(int *)(*(int *)(unaff_EBP + 8) + 0x33e5c),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x110c));
  FUN_0048a5dc((int *)(unaff_EBP + -0x1114),*(int *)(*(int *)(unaff_EBP + 8) + 0x33e5c),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x1110));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x33e5c); iVar6 = iVar6 + 1) {
    if (**(int **)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e6c) + iVar6 * 4) < 100) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   **(undefined1 **)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e6c) + iVar6 * 4));
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(char *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e6c) + iVar6 * 4) + 4)
                   + -100);
      *(undefined2 *)(unaff_EBP + -0x744) = 0x1184;
      FUN_00491944((int *)(unaff_EBP + -0x708));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
      FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x708));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      FUN_00491a74((int *)(unaff_EBP + -0x708),2);
      *(undefined2 *)(unaff_EBP + -0x744) = 0;
    }
    else {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   **(char **)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e6c) + iVar6 * 4) + -100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)
                    (*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e6c) + iVar6 * 4) + 4));
      *(undefined2 *)(unaff_EBP + -0x744) = 0x1190;
      FUN_00491944((int *)(unaff_EBP + -0x70c));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
      FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x70c));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      FUN_00491a74((int *)(unaff_EBP + -0x70c),2);
      *(undefined2 *)(unaff_EBP + -0x744) = 0;
    }
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x33e5c); iVar6 = iVar6 + 1) {
    FUN_0048a5dc((int *)(unaff_EBP + -0x111c),
                 *(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e64) + iVar6 * 4),0x100);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(unaff_EBP + -0x111c));
    FUN_0048a5dc((int *)(unaff_EBP + -0x1124),
                 *(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e64) + iVar6 * 4),0x100);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(unaff_EBP + -0x1120));
  }
  FUN_0048a5dc((int *)(unaff_EBP + -0x112c),*(int *)(*(int *)(unaff_EBP + 8) + 0x33e60),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x112c));
  FUN_0048a5dc((int *)(unaff_EBP + -0x1134),*(int *)(*(int *)(unaff_EBP + 8) + 0x33e60),0x100);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(undefined1 *)(unaff_EBP + -0x1130));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x33e60); iVar6 = iVar6 + 1) {
    if (**(int **)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e70) + iVar6 * 4) < 100) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   **(undefined1 **)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e70) + iVar6 * 4));
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(char *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e70) + iVar6 * 4) + 4)
                   + -100);
      *(undefined2 *)(unaff_EBP + -0x744) = 0x119c;
      FUN_00491944((int *)(unaff_EBP + -0x710));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
      FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x710));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      FUN_00491a74((int *)(unaff_EBP + -0x710),2);
      *(undefined2 *)(unaff_EBP + -0x744) = 0;
    }
    else {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   **(char **)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e70) + iVar6 * 4) + -100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)
                    (*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e70) + iVar6 * 4) + 4));
      *(undefined2 *)(unaff_EBP + -0x744) = 0x11a8;
      FUN_00491944((int *)(unaff_EBP + -0x714));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
      FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x714));
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      FUN_00491a74((int *)(unaff_EBP + -0x714),2);
      *(undefined2 *)(unaff_EBP + -0x744) = 0;
    }
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x33e60); iVar6 = iVar6 + 1) {
    FUN_0048a5dc((int *)(unaff_EBP + -0x113c),
                 *(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e68) + iVar6 * 4),0x100);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(unaff_EBP + -0x113c));
    FUN_0048a5dc((int *)(unaff_EBP + -0x1144),
                 *(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x33e68) + iVar6 * 4),0x100);
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(unaff_EBP + -0x1140));
  }
  iVar6 = 0;
  *(undefined4 *)(unaff_EBP + -0x1148) = 0;
  *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
  do {
    if (*(int *)(*(int *)(unaff_EBP + 8) + 0x3427c + iVar6 * 4) != 0) {
      *(int *)(unaff_EBP + -0x1148) = iVar6;
    }
    iVar6 = iVar6 + 1;
  } while (iVar6 < 0x40);
  FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
               *(char *)(unaff_EBP + -0x1148) + '\x01');
  iVar6 = 0;
  if (*(uint *)(unaff_EBP + -0x1148) < 0x80000000) {
    do {
      FUN_0048a5dc((int *)(unaff_EBP + -0x1150),
                   *(int *)(*(int *)(unaff_EBP + 8) + 0x3427c + iVar6 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x1150));
      FUN_0048a5dc((int *)(unaff_EBP + -0x1158),
                   *(int *)(*(int *)(unaff_EBP + 8) + 0x3427c + iVar6 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x1154));
      iVar6 = iVar6 + 1;
    } while (iVar6 <= *(int *)(unaff_EBP + -0x1148));
  }
  iVar6 = 0;
  if (*(uint *)(unaff_EBP + -0x1148) < 0x80000000) {
    do {
      FUN_0048a5dc((int *)(unaff_EBP + -0x1160),
                   *(int *)(*(int *)(unaff_EBP + 8) + 0x3437c + iVar6 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x1160));
      FUN_0048a5dc((int *)(unaff_EBP + -0x1168),
                   *(int *)(*(int *)(unaff_EBP + 8) + 0x3437c + iVar6 * 4),0x100);
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                   *(undefined1 *)(unaff_EBP + -0x1164));
      iVar6 = iVar6 + 1;
    } while (iVar6 <= *(int *)(unaff_EBP + -0x1148));
  }
  iVar6 = 0;
  if (*(uint *)(unaff_EBP + -0x1148) < 0x80000000) {
    do {
      for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0x3437c + iVar6 * 4);
          iVar7 = iVar7 + 1) {
        FUN_0048a5dc((int *)(unaff_EBP + -0x1170),
                     *(int *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x3447c) + iVar6 * 4) +
                             iVar7 * 4),0x100);
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                     *(undefined1 *)(unaff_EBP + -0x1170));
        FUN_0048a5dc((int *)(unaff_EBP + -0x1178),
                     *(int *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x3447c) + iVar6 * 4) +
                             iVar7 * 4),0x100);
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                     *(undefined1 *)(unaff_EBP + -0x1174));
      }
      iVar6 = iVar6 + 1;
    } while (iVar6 <= *(int *)(unaff_EBP + -0x1148));
  }
  iVar6 = 0;
  if (*(uint *)(unaff_EBP + -0x1148) < 0x80000000) {
    do {
      for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0x3437c + iVar6 * 4);
          iVar7 = iVar7 + 1) {
        *(undefined2 *)(unaff_EBP + -0x744) = 0x11b4;
        FUN_00491944((int *)(unaff_EBP + -0x718));
        *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
        FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x718));
        *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
        FUN_00491a74((int *)(unaff_EBP + -0x718),2);
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),0);
        *(undefined2 *)(unaff_EBP + -0x744) = 0;
      }
      iVar6 = iVar6 + 1;
    } while (iVar6 <= *(int *)(unaff_EBP + -0x1148));
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar6 = iVar6 + 1) {
    iVar8 = 0;
    *(undefined4 *)(unaff_EBP + -0x117c) = 1;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
    iVar7 = 0;
    do {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x40 + 0x34484 + iVar7) *
                      *(int *)(unaff_EBP + -0x117c);
      *(int *)(unaff_EBP + -0x117c) = *(int *)(unaff_EBP + -0x117c) * 2;
      if (*(int *)(unaff_EBP + -0x117c) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x117c) = 1;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    if (*(int *)(unaff_EBP + -0x117c) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
  }
  iVar6 = 0;
  do {
    iVar8 = 0;
    *(undefined4 *)(unaff_EBP + -0x1180) = 1;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
    for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar7 = iVar7 + 1) {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x200 + 0x3c484 + iVar7) *
                      *(int *)(unaff_EBP + -0x1180);
      *(int *)(unaff_EBP + -0x1180) = *(int *)(unaff_EBP + -0x1180) * 2;
      if (*(int *)(unaff_EBP + -0x1180) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x1180) = 1;
      }
    }
    if (*(int *)(unaff_EBP + -0x1180) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
    iVar6 = iVar6 + 1;
  } while (iVar6 < 0x40);
  iVar6 = 0;
  do {
    iVar8 = 0;
    *(undefined4 *)(unaff_EBP + -0x1184) = 1;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
    iVar7 = 0;
    do {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x40 + 0x44484 + iVar7) *
                      *(int *)(unaff_EBP + -0x1184);
      *(int *)(unaff_EBP + -0x1184) = *(int *)(unaff_EBP + -0x1184) * 2;
      if (*(int *)(unaff_EBP + -0x1184) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x1184) = 1;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    if (*(int *)(unaff_EBP + -0x1184) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
    iVar6 = iVar6 + 1;
  } while (iVar6 < 0x40);
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar6 = iVar6 + 1) {
    iVar8 = 0;
    *(undefined4 *)(unaff_EBP + -0x1188) = 1;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
    for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar7 = iVar7 + 1) {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(unaff_EBP + 8) + iVar6 * 0x200 + 0x45484 + iVar7) *
                      *(int *)(unaff_EBP + -0x1188);
      *(int *)(unaff_EBP + -0x1188) = *(int *)(unaff_EBP + -0x1188) * 2;
      if (*(int *)(unaff_EBP + -0x1188) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x1188) = 1;
      }
    }
    if (*(int *)(unaff_EBP + -0x1188) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x33e60); iVar6 = iVar6 + 1) {
    iVar8 = 0;
    *(undefined4 *)(unaff_EBP + -0x118c) = 1;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
    for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar7 = iVar7 + 1) {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x85484) +
                                             iVar6 * 4) + iVar7) * *(int *)(unaff_EBP + -0x118c);
      *(int *)(unaff_EBP + -0x118c) = *(int *)(unaff_EBP + -0x118c) * 2;
      if (*(int *)(unaff_EBP + -0x118c) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x118c) = 1;
      }
    }
    if (*(int *)(unaff_EBP + -0x118c) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
    iVar8 = 0;
    iVar7 = 0;
    *(undefined4 *)(unaff_EBP + -0x118c) = 1;
    do {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x85484) +
                                             iVar6 * 4) + 100 + iVar7) *
                      *(int *)(unaff_EBP + -0x118c);
      *(int *)(unaff_EBP + -0x118c) = *(int *)(unaff_EBP + -0x118c) * 2;
      if (*(int *)(unaff_EBP + -0x118c) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x118c) = 1;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    if (*(int *)(unaff_EBP + -0x118c) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
  }
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x33e60); iVar6 = iVar6 + 1) {
    iVar8 = 0;
    *(undefined4 *)(unaff_EBP + -0x1190) = 1;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
    for (iVar7 = 0; iVar7 < *(int *)(*(int *)(unaff_EBP + 8) + 0x44); iVar7 = iVar7 + 1) {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x85488) +
                                             iVar6 * 4) + iVar7) * *(int *)(unaff_EBP + -0x1190);
      *(int *)(unaff_EBP + -0x1190) = *(int *)(unaff_EBP + -0x1190) * 2;
      if (*(int *)(unaff_EBP + -0x1190) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x1190) = 1;
      }
    }
    if (*(int *)(unaff_EBP + -0x1190) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
    iVar8 = 0;
    iVar7 = 0;
    *(undefined4 *)(unaff_EBP + -0x1190) = 1;
    do {
      iVar8 = iVar8 + (int)*(char *)(*(int *)(*(int *)(*(int *)(unaff_EBP + 8) + 0x85488) +
                                             iVar6 * 4) + 100 + iVar7) *
                      *(int *)(unaff_EBP + -0x1190);
      *(int *)(unaff_EBP + -0x1190) = *(int *)(unaff_EBP + -0x1190) * 2;
      if (*(int *)(unaff_EBP + -0x1190) == 0x100) {
        FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
        iVar8 = 0;
        *(undefined4 *)(unaff_EBP + -0x1190) = 1;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    if (*(int *)(unaff_EBP + -0x1190) != 1) {
      FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),(char)iVar8);
    }
  }
  iVar6 = 0;
  do {
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x33e74 + iVar6 * 4));
    iVar6 = iVar6 + 1;
  } while (iVar6 < 0x7f);
  iVar6 = 0;
  do {
    FUN_00429f74(*(undefined4 *)(unaff_EBP + 8),(int *)(unaff_EBP + -0x1c),
                 *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x34078 + iVar6 * 4));
    iVar6 = iVar6 + 1;
  } while (iVar6 < 0x7f);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x11c0;
  FUN_00491944((int *)(unaff_EBP + -0x71c));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  FUN_00491ab8((int *)(unaff_EBP + -0x1c),(undefined4 *)(unaff_EBP + -0x71c));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x71c),2);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x11cc;
  piVar1 = FUN_00491944((int *)(unaff_EBP + -0x720));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 1;
  uVar2 = FUN_0047c5dc((undefined *)*piVar1);
  *(undefined4 *)(unaff_EBP + -0x7a8) = uVar2;
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x720),2);
  FUN_0047c658(*(HANDLE *)(unaff_EBP + -0x7a8),0,0);
  DVar3 = FUN_00491bfc((int *)(unaff_EBP + -0x1c));
  if (*(int *)(unaff_EBP + -0x1c) == 0) {
    puVar5 = &DAT_0049859d;
  }
  else {
    puVar5 = *(undefined **)(unaff_EBP + -0x1c);
  }
  FUN_0047c62c(*(HANDLE *)(unaff_EBP + -0x7a8),puVar5,DVar3);
  FUN_0047c664(*(HANDLE *)(unaff_EBP + -0x7a8));
  *(undefined4 *)(unaff_EBP + -0x724) = *(undefined4 *)(unaff_EBP + -0x7f0);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x11e4;
  FUN_00483918(*(int *)(unaff_EBP + -0x724),8,0,0x19,FUN_0040be6c);
  *(undefined2 *)(unaff_EBP + -0x744) = 0x11d8;
  FUN_00483674(*(int *)(unaff_EBP + -0x7f4));
  for (iVar6 = 0; iVar6 < *(int *)(*(int *)(unaff_EBP + 8) + 0x3c) * 3; iVar6 = iVar6 + 1) {
    FUN_00483674(*(int *)(*(int *)(unaff_EBP + -0x7f8) + iVar6 * 4));
  }
  FUN_00483674(*(int *)(unaff_EBP + -0x7f8));
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00491a74((int *)(unaff_EBP + -0x1c),2);
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  *(int *)(unaff_EBP + -0x1194) = *(int *)(unaff_EBP + -0x14) + -0x2c;
  InterlockedDecrement((LONG *)(*(int *)(unaff_EBP + -0x1194) + 0x1c));
  if (*(int *)(*(int *)(unaff_EBP + -0x1194) + 0x1c) == -1) {
    *(int *)(unaff_EBP + -0x1198) = *(int *)(unaff_EBP + -0x14) + -0x2c;
    *(undefined2 *)(unaff_EBP + -0x744) = 0x11fc;
    FUN_00406f0c(unaff_EBP + -0x728);
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 2;
    *(undefined4 *)(unaff_EBP + -0x730) = *(undefined4 *)(unaff_EBP + -0x1198);
    if (*(int *)(unaff_EBP + -0x730) != 0) {
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      *(undefined2 *)(unaff_EBP + -0x744) = 0x1208;
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
      if (*(int *)(*(int *)(unaff_EBP + -0x730) + 0x18) != 0) {
        *(undefined4 *)(*(int *)(unaff_EBP + -0x730) + 0x18) = 0;
        DeleteCriticalSection(*(LPCRITICAL_SECTION *)(unaff_EBP + -0x730));
      }
      *(undefined2 *)(unaff_EBP + -0x744) = 0x11fc;
    }
    *(undefined4 *)(unaff_EBP + -0x119c) = *(undefined4 *)(*(int *)(unaff_EBP + -0x14) + -8);
    *(int *)(unaff_EBP + -0x11a0) = *(int *)(unaff_EBP + -0x14) + -0x2c;
    uVar2 = FUN_00406f48(unaff_EBP + -0x72c);
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + 2;
    *(undefined4 *)(unaff_EBP + -0x11a4) = uVar2;
    FUN_00483664(*(int *)(unaff_EBP + -0x11a0));
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    FUN_00406b38(unaff_EBP + -0x72c,2);
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
    FUN_00406b38(unaff_EBP + -0x728,2);
    *(undefined2 *)(unaff_EBP + -0x744) = 0x11f0;
  }
  *(undefined2 *)(unaff_EBP + -0x744) = 0x110;
  *(int *)(unaff_EBP + -0x738) = *(int *)(unaff_EBP + -0x738) + -1;
  FUN_00406b38(unaff_EBP + -0x18,2);
  *(undefined2 *)(unaff_EBP + -0x744) = 8;
  FUN_00483674(*(int *)(unaff_EBP + -0x758));
  *(undefined1 *)(*(int *)(unaff_EBP + 8) + 0x8549a) = 0;
  **(undefined1 **)(unaff_EBP + 8) = 1;
  *in_FS_OFFSET = *(undefined4 *)(unaff_EBP + -0x754);
  return;
}


