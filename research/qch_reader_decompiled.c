// FUN_0041cd90 @ 0041cd90

void __cdecl FUN_0041cd90(int param_1,int param_2)

{
  undefined4 uVar1;
  int *piVar2;
  byte *pbVar3;
  byte *pbVar4;
  uint uVar5;
  char *pcVar6;
  int iVar7;
  int iVar8;
  undefined4 *in_FS_OFFSET;
  byte *local_a0;
  byte *local_9c;
  int local_98;
  byte *local_94;
  int local_90;
  byte *local_8c;
  int local_88;
  byte *local_84;
  int local_80;
  byte *local_7c;
  char *local_78;
  byte *local_70;
  uint *local_68;
  int *local_64;
  uint *local_60;
  int *local_5c;
  uint *local_58;
  char *local_54;
  char *local_50;
  char *local_4c;
  char *local_48;
  char *local_44;
  char *local_40;
  int local_30;
  undefined4 local_2c;
  
  FUN_004870a0(0x49b634);
  iVar8 = 2;
  do {
    iVar7 = iVar8 + 1;
    pcVar6 = (char *)(param_2 + iVar8);
    iVar8 = iVar7;
  } while (*pcVar6 != '\0');
  FUN_00485a9c(param_1 + 0xc,(uint *)&DAT_0049859e);
  FUN_00485a9c(param_1 + 0x14,(uint *)&DAT_0049859f);
  FUN_00485a9c(param_1 + 0x1c,(uint *)&DAT_004985a0);
  FUN_00485a9c(param_1 + 0x24,(uint *)&DAT_004985a1);
  FUN_00485a9c(param_1 + 0x34,(uint *)&DAT_004985a2);
  local_40 = (char *)(param_2 + iVar7);
  while (*local_40 != '\0') {
    local_40 = local_40 + 1;
    FUN_00429f10(param_1,param_1 + 0xc,*(undefined1 *)(param_2 + iVar7));
    iVar7 = iVar7 + 1;
  }
  local_44 = (char *)(param_2 + iVar7 + 1);
  iVar8 = iVar7 + 1;
  while (*local_44 != '\0') {
    local_44 = local_44 + 1;
    FUN_00429f10(param_1,param_1 + 0x14,*(undefined1 *)(param_2 + iVar8));
    iVar8 = iVar8 + 1;
  }
  local_48 = (char *)(param_2 + iVar8 + 1);
  iVar8 = iVar8 + 1;
  while (*local_48 != '\0') {
    local_48 = local_48 + 1;
    FUN_00429f10(param_1,param_1 + 0x1c,*(undefined1 *)(param_2 + iVar8));
    iVar8 = iVar8 + 1;
  }
  local_4c = (char *)(param_2 + iVar8 + 1);
  iVar8 = iVar8 + 1;
  while (*local_4c != '\0') {
    local_4c = local_4c + 1;
    FUN_00429f10(param_1,param_1 + 0x24,*(undefined1 *)(param_2 + iVar8));
    iVar8 = iVar8 + 1;
  }
  local_50 = (char *)(param_2 + iVar8 + 1);
  iVar8 = iVar8 + 1;
  while (*local_50 != '\0') {
    local_50 = local_50 + 1;
    FUN_00429f10(param_1,param_1 + 0x34,*(undefined1 *)(param_2 + iVar8));
    iVar8 = iVar8 + 1;
  }
  iVar7 = iVar8 + 1;
  *(bool *)(param_1 + 0x4c) = (*(byte *)(param_2 + iVar7) & 1) != 0;
  *(bool *)(param_1 + 0x4d) = (*(byte *)(param_2 + iVar7) & 2) != 0;
  *(bool *)(param_1 + 0x4e) = (*(byte *)(param_2 + iVar7) & 4) != 0;
  *(bool *)(param_1 + 0x4f) = (*(byte *)(param_2 + iVar7) & 8) != 0;
  *(bool *)(param_1 + 0x50) = (*(byte *)(param_2 + iVar7) & 0x10) != 0;
  *(bool *)(param_1 + 1) = (*(byte *)(param_2 + iVar7) & 0x80) != 0;
  *(uint *)(param_1 + 0x54) = (uint)*(byte *)(param_2 + iVar8 + 2);
  *(uint *)(param_1 + 0x58) = (uint)*(byte *)(param_2 + iVar8 + 3);
  *(uint *)(param_1 + 0x5c) = (uint)*(byte *)(param_2 + iVar8 + 4);
  *(undefined1 *)(param_1 + 0x85498) = *(undefined1 *)(param_2 + iVar8 + 5);
  *(undefined1 *)(param_1 + 0x85499) = *(undefined1 *)(param_2 + iVar8 + 6);
  FUN_00485a9c(param_1 + 0x60,(uint *)&DAT_004985a3);
  local_54 = (char *)(param_2 + iVar8 + 7);
  iVar8 = iVar8 + 7;
  while (*local_54 != '\0') {
    local_54 = local_54 + 1;
    FUN_00429f10(param_1,param_1 + 0x60,*(undefined1 *)(param_2 + iVar8));
    iVar8 = iVar8 + 1;
  }
  *(uint *)(param_1 + 0x3c) = (uint)*(byte *)(param_2 + iVar8 + 1) << 8;
  *(int *)(param_1 + 0x3c) = *(int *)(param_1 + 0x3c) + (uint)*(byte *)(param_2 + iVar8 + 2);
  *(uint *)(param_1 + 0xe58) = (uint)*(byte *)(param_2 + iVar8 + 3);
  if (*(int *)(param_1 + 0x3c) < 0x101) {
    uVar1 = 0x100;
  }
  else {
    uVar1 = *(undefined4 *)(param_1 + 0x3c);
  }
  *(undefined4 *)(param_1 + 0x40) = uVar1;
  uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
  *(undefined4 *)(param_1 + 0x33e64) = uVar1;
  uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
  *(undefined4 *)(param_1 + 0x33e68) = uVar1;
  uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
  *(undefined4 *)(param_1 + 0x33e6c) = uVar1;
  uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
  *(undefined4 *)(param_1 + 0x33e70) = uVar1;
  uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
  *(undefined4 *)(param_1 + 0x85484) = uVar1;
  uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
  *(undefined4 *)(param_1 + 0x85488) = uVar1;
  uVar1 = FUN_004836cc(0x100);
  *(undefined4 *)(param_1 + 0x3447c) = uVar1;
  uVar1 = FUN_004836cc(0x100);
  *(undefined4 *)(param_1 + 0x34480) = uVar1;
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x40); local_30 = local_30 + 1) {
    uVar1 = FUN_004836cc(8);
    *(undefined4 *)(*(int *)(param_1 + 0x33e6c) + local_30 * 4) = uVar1;
    uVar1 = FUN_004836cc(8);
    *(undefined4 *)(*(int *)(param_1 + 0x33e70) + local_30 * 4) = uVar1;
    uVar1 = FUN_004836cc(0xa4);
    *(undefined4 *)(*(int *)(param_1 + 0x85484) + local_30 * 4) = uVar1;
    uVar1 = FUN_004836cc(0xa4);
    *(undefined4 *)(*(int *)(param_1 + 0x85488) + local_30 * 4) = uVar1;
  }
  local_30 = 0;
  do {
    uVar1 = FUN_004836cc(*(int *)(param_1 + 0x40) << 2);
    *(undefined4 *)(*(int *)(param_1 + 0x3447c) + local_30 * 4) = uVar1;
    piVar2 = (int *)FUN_004836cc(*(int *)(param_1 + 0x40) * 8 + 4);
    if (piVar2 != (int *)0x0) {
      FUN_00483a78(piVar2,8,*(int *)(param_1 + 0x40),0x211,FUN_0040d9dc);
    }
    *(int **)(*(int *)(param_1 + 0x34480) + local_30 * 4) = piVar2;
    local_30 = local_30 + 1;
  } while (local_30 < 0x40);
  iVar7 = iVar8 + 5;
  *(uint *)(param_1 + 0x68) = (uint)*(byte *)(param_2 + iVar8 + 4);
  local_58 = (uint *)(param_1 + 0x86c);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x68); local_30 = local_30 + 1) {
    FUN_00485a9c(local_30 * 8 + param_1 + 0x6c,(uint *)&DAT_004985a4);
    iVar8 = iVar7;
    for (pcVar6 = (char *)(param_2 + iVar7); *pcVar6 != '\0'; pcVar6 = pcVar6 + 1) {
      FUN_00429f10(param_1,local_30 * 8 + param_1 + 0x6c,*(undefined1 *)(param_2 + iVar8));
      iVar8 = iVar8 + 1;
    }
    iVar7 = iVar8 + 2;
    *local_58 = (uint)*(byte *)(param_2 + iVar8 + 1);
    local_58 = local_58 + 1;
  }
  *(uint *)(param_1 + 0x44) = (uint)*(byte *)(param_2 + iVar7);
  for (local_30 = 0; iVar7 = iVar7 + 1, local_30 < *(int *)(param_1 + 0x44); local_30 = local_30 + 1
      ) {
    FUN_00485a9c(local_30 * 8 + param_1 + 0xe5c,(uint *)&DAT_004985a5);
    pcVar6 = (char *)(param_2 + iVar7);
    for (; *pcVar6 != '\0'; pcVar6 = pcVar6 + 1) {
      FUN_00429f10(param_1,local_30 * 8 + param_1 + 0xe5c,*(undefined1 *)(param_2 + iVar7));
      iVar7 = iVar7 + 1;
    }
  }
  local_60 = (uint *)(param_1 + 0x3e5c);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x44); local_30 = local_30 + 1) {
    local_5c = (int *)local_60;
    pbVar4 = (byte *)(param_2 + iVar7);
    for (iVar8 = 0; iVar8 < *(int *)(param_1 + 0xe58); iVar8 = iVar8 + 1) {
      pbVar3 = pbVar4 + 1;
      *local_5c = (uint)*pbVar4 << 8;
      pbVar4 = pbVar4 + 2;
      iVar7 = iVar7 + 2;
      *local_5c = *local_5c + (uint)*pbVar3;
      local_5c = local_5c + 1;
    }
    local_60 = local_60 + 0x20;
  }
  *(uint *)(param_1 + 0x48) = (uint)*(byte *)(param_2 + iVar7) << 8;
  iVar8 = iVar7 + 2;
  *(int *)(param_1 + 0x48) = *(int *)(param_1 + 0x48) + (uint)*(byte *)(param_2 + iVar7 + 1);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x48); local_30 = local_30 + 1) {
    FUN_00485a9c(local_30 * 8 + param_1 + 0x1e5c,(uint *)&DAT_004985a6);
    pcVar6 = (char *)(param_2 + iVar8);
    for (; *pcVar6 != '\0'; pcVar6 = pcVar6 + 1) {
      FUN_00429f10(param_1,local_30 * 8 + param_1 + 0x1e5c,*(undefined1 *)(param_2 + iVar8));
      iVar8 = iVar8 + 1;
    }
    iVar8 = iVar8 + 1;
  }
  local_68 = (uint *)(param_1 + 0x13e5c);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x48); local_30 = local_30 + 1) {
    local_64 = (int *)local_68;
    pbVar4 = (byte *)(param_2 + iVar8);
    for (iVar7 = 0; iVar7 < *(int *)(param_1 + 0xe58); iVar7 = iVar7 + 1) {
      pbVar3 = pbVar4 + 1;
      *local_64 = (uint)*pbVar4 << 8;
      pbVar4 = pbVar4 + 2;
      iVar8 = iVar8 + 2;
      *local_64 = *local_64 + (uint)*pbVar3;
      local_64 = local_64 + 1;
    }
    local_68 = local_68 + 0x20;
  }
  *(uint *)(param_1 + 0xe04) = (uint)*(byte *)(param_2 + iVar8);
  for (local_30 = 0; iVar7 = iVar8 + 1, local_30 < *(int *)(param_1 + 0xe04);
      local_30 = local_30 + 1) {
    FUN_00485a9c(local_30 * 8 + param_1 + 0xe08,(uint *)&DAT_004985a7);
    iVar8 = iVar7;
    for (pcVar6 = (char *)(param_2 + iVar7); *pcVar6 != '\0'; pcVar6 = pcVar6 + 1) {
      FUN_00429f10(param_1,local_30 * 8 + param_1 + 0xe08,*(undefined1 *)(param_2 + iVar8));
      iVar8 = iVar8 + 1;
    }
  }
  *(uint *)(param_1 + 0x33e5c) = (uint)*(byte *)(param_2 + iVar7) << 8;
  iVar7 = iVar8 + 3;
  *(int *)(param_1 + 0x33e5c) = *(int *)(param_1 + 0x33e5c) + (uint)*(byte *)(param_2 + iVar8 + 2);
  local_68 = (uint *)(param_2 + iVar7);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x33e5c); local_30 = local_30 + 1) {
    **(uint **)(*(int *)(param_1 + 0x33e6c) + local_30 * 4) = (uint)(byte)*local_68;
    *(uint *)(*(int *)(*(int *)(param_1 + 0x33e6c) + local_30 * 4) + 4) =
         (uint)*(byte *)((int)local_68 + 1);
    pbVar4 = (byte *)((int)local_68 + 2);
    iVar7 = iVar7 + 3;
    local_68 = (uint *)((int)local_68 + 3);
    if (*pbVar4 == 0x56) {
      piVar2 = (int *)(*(int *)(*(int *)(param_1 + 0x33e6c) + local_30 * 4) + 4);
      *piVar2 = *piVar2 + 100;
    }
    else {
      piVar2 = *(int **)(*(int *)(param_1 + 0x33e6c) + local_30 * 4);
      *piVar2 = *piVar2 + 100;
    }
  }
  local_68 = (uint *)(param_2 + iVar7);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x33e5c); local_30 = local_30 + 1) {
    iVar7 = iVar7 + 2;
    *(uint *)(*(int *)(param_1 + 0x33e64) + local_30 * 4) = (uint)(byte)*local_68 << 8;
    piVar2 = (int *)(*(int *)(param_1 + 0x33e64) + local_30 * 4);
    *piVar2 = *piVar2 + (uint)*(byte *)((int)local_68 + 1);
    local_68 = (uint *)((int)local_68 + 2);
  }
  *(uint *)(param_1 + 0x33e60) = (uint)*(byte *)(param_2 + iVar7) << 8;
  iVar8 = iVar7 + 2;
  *(int *)(param_1 + 0x33e60) = *(int *)(param_1 + 0x33e60) + (uint)*(byte *)(param_2 + iVar7 + 1);
  local_68 = (uint *)(param_2 + iVar8);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x33e60); local_30 = local_30 + 1) {
    **(uint **)(*(int *)(param_1 + 0x33e70) + local_30 * 4) = (uint)(byte)*local_68;
    *(uint *)(*(int *)(*(int *)(param_1 + 0x33e70) + local_30 * 4) + 4) =
         (uint)*(byte *)((int)local_68 + 1);
    pbVar4 = (byte *)((int)local_68 + 2);
    iVar8 = iVar8 + 3;
    local_68 = (uint *)((int)local_68 + 3);
    if (*pbVar4 == 0x56) {
      piVar2 = (int *)(*(int *)(*(int *)(param_1 + 0x33e70) + local_30 * 4) + 4);
      *piVar2 = *piVar2 + 100;
    }
    else {
      piVar2 = *(int **)(*(int *)(param_1 + 0x33e70) + local_30 * 4);
      *piVar2 = *piVar2 + 100;
    }
  }
  local_68 = (uint *)(param_2 + iVar8);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x33e60); local_30 = local_30 + 1) {
    iVar8 = iVar8 + 2;
    *(uint *)(*(int *)(param_1 + 0x33e68) + local_30 * 4) = (uint)(byte)*local_68 << 8;
    piVar2 = (int *)(*(int *)(param_1 + 0x33e68) + local_30 * 4);
    *piVar2 = *piVar2 + (uint)*(byte *)((int)local_68 + 1);
    local_68 = (uint *)((int)local_68 + 2);
  }
  uVar5 = (uint)*(byte *)(param_2 + iVar8);
  local_30 = 0;
  local_60 = (uint *)(param_1 + 0x3427c);
  iVar8 = iVar8 + 1;
  local_68 = (uint *)(param_2 + iVar8);
  if (uVar5 != 0) {
    do {
      iVar8 = iVar8 + 2;
      *local_60 = (uint)(byte)*local_68 << 8;
      *local_60 = *local_60 + (uint)*(byte *)((int)local_68 + 1);
      local_68 = (uint *)((int)local_68 + 2);
      local_30 = local_30 + 1;
      local_60 = local_60 + 1;
    } while (local_30 < (int)uVar5);
  }
  local_68 = (uint *)(param_1 + 0x3437c);
  local_30 = 0;
  local_60 = (uint *)(param_2 + iVar8);
  if (uVar5 != 0) {
    do {
      iVar8 = iVar8 + 2;
      *local_68 = (uint)(byte)*local_60 << 8;
      *local_68 = *local_68 + (uint)*(byte *)((int)local_60 + 1);
      local_60 = (uint *)((int)local_60 + 2);
      local_30 = local_30 + 1;
      local_68 = local_68 + 1;
    } while (local_30 < (int)uVar5);
  }
  local_68 = (uint *)(param_1 + 0x3437c);
  local_30 = 0;
  if (uVar5 != 0) {
    do {
      local_70 = (byte *)(param_2 + iVar8);
      for (iVar7 = 0; iVar7 < (int)*local_68; iVar7 = iVar7 + 1) {
        *(uint *)(*(int *)(*(int *)(param_1 + 0x3447c) + local_30 * 4) + iVar7 * 4) =
             (uint)*local_70 << 8;
        piVar2 = (int *)(*(int *)(*(int *)(param_1 + 0x3447c) + local_30 * 4) + iVar7 * 4);
        *piVar2 = *piVar2 + (uint)local_70[1];
        iVar8 = iVar8 + 2;
        local_70 = local_70 + 2;
      }
      local_30 = local_30 + 1;
      local_68 = local_68 + 1;
    } while (local_30 < (int)uVar5);
  }
  local_68 = (uint *)(param_1 + 0x3437c);
  local_30 = 0;
  if (uVar5 != 0) {
    do {
      for (iVar7 = 0; iVar7 < (int)*local_68; iVar7 = iVar7 + 1) {
        FUN_00485a9c(*(int *)(*(int *)(param_1 + 0x34480) + local_30 * 4) + iVar7 * 8,
                     (uint *)&DAT_004985a8);
        local_78 = (char *)(param_2 + iVar8);
        while (*local_78 != '\0') {
          local_78 = local_78 + 1;
          FUN_00429f10(param_1,*(int *)(*(int *)(param_1 + 0x34480) + local_30 * 4) + iVar7 * 8,
                       *(undefined1 *)(param_2 + iVar8));
          iVar8 = iVar8 + 1;
        }
        iVar8 = iVar8 + 1;
      }
      local_30 = local_30 + 1;
      local_68 = local_68 + 1;
    } while (local_30 < (int)uVar5);
  }
  local_68 = (uint *)(param_1 + 0x34484);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x44); local_30 = local_30 + 1) {
    uVar5 = 1;
    iVar7 = 0;
    local_80 = (int)local_68;
    local_7c = (byte *)(param_2 + iVar8);
    do {
      *(bool *)local_80 = (*local_7c & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_7c = local_7c + 1;
      }
      iVar7 = iVar7 + 1;
      local_80 = local_80 + 1;
    } while (iVar7 < 0x40);
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
    local_68 = (uint *)((int)local_68 + 0x40);
  }
  local_68 = (uint *)(param_1 + 0x3c484);
  local_30 = 0;
  do {
    uVar5 = 1;
    local_88 = (int)local_68;
    local_84 = (byte *)(param_2 + iVar8);
    for (iVar7 = 0; iVar7 < *(int *)(param_1 + 0x44); iVar7 = iVar7 + 1) {
      *(bool *)local_88 = (*local_84 & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_84 = local_84 + 1;
      }
      local_88 = local_88 + 1;
    }
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
    local_30 = local_30 + 1;
    local_68 = (uint *)((int)local_68 + 0x200);
  } while (local_30 < 0x40);
  local_68 = (uint *)(param_1 + 0x44484);
  local_30 = 0;
  do {
    uVar5 = 1;
    iVar7 = 0;
    local_90 = (int)local_68;
    local_8c = (byte *)(param_2 + iVar8);
    do {
      *(bool *)local_90 = (*local_8c & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_8c = local_8c + 1;
      }
      iVar7 = iVar7 + 1;
      local_90 = local_90 + 1;
    } while (iVar7 < 0x40);
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
    local_30 = local_30 + 1;
    local_68 = (uint *)((int)local_68 + 0x40);
  } while (local_30 < 0x40);
  local_68 = (uint *)(param_1 + 0x45484);
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x44); local_30 = local_30 + 1) {
    uVar5 = 1;
    local_98 = (int)local_68;
    local_94 = (byte *)(param_2 + iVar8);
    for (iVar7 = 0; iVar7 < *(int *)(param_1 + 0x44); iVar7 = iVar7 + 1) {
      *(bool *)local_98 = (*local_94 & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_94 = local_94 + 1;
      }
      local_98 = local_98 + 1;
    }
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
    local_68 = (uint *)((int)local_68 + 0x200);
  }
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x33e60); local_30 = local_30 + 1) {
    uVar5 = 1;
    local_9c = (byte *)(param_2 + iVar8);
    for (iVar7 = 0; iVar7 < *(int *)(param_1 + 0x44); iVar7 = iVar7 + 1) {
      *(bool *)(*(int *)(*(int *)(param_1 + 0x85484) + local_30 * 4) + iVar7) =
           (*local_9c & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_9c = local_9c + 1;
      }
    }
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
    uVar5 = 1;
    iVar7 = 0;
    local_9c = (byte *)(param_2 + iVar8);
    do {
      *(bool *)(*(int *)(*(int *)(param_1 + 0x85484) + local_30 * 4) + 100 + iVar7) =
           (*local_9c & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_9c = local_9c + 1;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
  }
  for (local_30 = 0; local_30 < *(int *)(param_1 + 0x33e60); local_30 = local_30 + 1) {
    uVar5 = 1;
    local_a0 = (byte *)(param_2 + iVar8);
    for (iVar7 = 0; iVar7 < *(int *)(param_1 + 0x44); iVar7 = iVar7 + 1) {
      *(bool *)(*(int *)(*(int *)(param_1 + 0x85488) + local_30 * 4) + iVar7) =
           (*local_a0 & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_a0 = local_a0 + 1;
      }
    }
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
    uVar5 = 1;
    iVar7 = 0;
    local_a0 = (byte *)(param_2 + iVar8);
    do {
      *(bool *)(*(int *)(*(int *)(param_1 + 0x85488) + local_30 * 4) + 100 + iVar7) =
           (*local_a0 & uVar5) != 0;
      uVar5 = uVar5 * 2;
      if (uVar5 == 0x100) {
        uVar5 = 1;
        iVar8 = iVar8 + 1;
        local_a0 = local_a0 + 1;
      }
      iVar7 = iVar7 + 1;
    } while (iVar7 < 0x40);
    if (uVar5 != 1) {
      iVar8 = iVar8 + 1;
    }
  }
  local_60 = (uint *)(param_1 + 0x33e74);
  local_30 = 0;
  local_68 = (uint *)(param_2 + iVar8);
  do {
    iVar8 = iVar8 + 1;
    *local_60 = (uint)(byte)*local_68;
    local_68 = (uint *)((int)local_68 + 1);
    local_30 = local_30 + 1;
    local_60 = local_60 + 1;
  } while (local_30 < 0x7f);
  local_68 = (uint *)(param_1 + 0x34078);
  local_30 = 0;
  local_60 = (uint *)(param_2 + iVar8);
  do {
    *local_68 = (uint)(byte)*local_60;
    local_60 = (uint *)((int)local_60 + 1);
    local_30 = local_30 + 1;
    local_68 = local_68 + 1;
  } while (local_30 < 0x7f);
  _TCGauge_SetProgress_qqrl(*(int **)(*(int *)(param_1 + 0x855b4) + 0x1e8),0x10);
  *in_FS_OFFSET = local_2c;
  return;
}


