// FUN_0040da38 @ 0040da38

undefined1 * __cdecl FUN_0040da38(undefined1 *param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int *piVar2;
  int iVar3;
  undefined4 *in_FS_OFFSET;
  undefined4 local_54;
  undefined1 local_2c [4];
  undefined1 local_28 [4];
  undefined1 local_24 [4];
  undefined1 local_20 [4];
  undefined1 local_1c [4];
  undefined1 local_18 [4];
  undefined1 local_14 [4];
  undefined1 local_10 [4];
  undefined1 local_c [4];
  undefined1 local_8 [4];
  
  FUN_004870a0(0x4988c4);
  FUN_00406b70(local_8);
  FUN_00406b98(param_1 + 4);
  *(undefined1 **)(param_1 + 8) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_c);
  FUN_00406b98(param_1 + 0xc);
  *(undefined1 **)(param_1 + 0x10) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_10);
  FUN_00406b98(param_1 + 0x14);
  *(undefined1 **)(param_1 + 0x18) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_14);
  FUN_00406b98(param_1 + 0x1c);
  *(undefined1 **)(param_1 + 0x20) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_18);
  FUN_00406b98(param_1 + 0x24);
  *(undefined1 **)(param_1 + 0x28) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_1c);
  FUN_00406b98(param_1 + 0x2c);
  *(undefined1 **)(param_1 + 0x30) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_20);
  FUN_00406b98(param_1 + 0x34);
  *(undefined1 **)(param_1 + 0x38) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_24);
  FUN_00406b98(param_1 + 0x60);
  *(undefined1 **)(param_1 + 100) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00483a78((int *)(param_1 + 0x6c),8,0x100,1,FUN_0040d9dc);
  FUN_00483a78((int *)(param_1 + 0xc6c),4,100,3,_System_AnsiString__bctr_qqrv);
  FUN_00483a78((int *)(param_1 + 0xe08),8,10,1,FUN_0040d9dc);
  FUN_00483a78((int *)(param_1 + 0xe5c),8,0x200,1,FUN_0040d9dc);
  FUN_00483a78((int *)(param_1 + 0x1e5c),8,0x400,1,FUN_0040d9dc);
  FUN_00406b70(local_28);
  FUN_00406b98(param_1 + 0x8548c);
  *(undefined1 **)(param_1 + 0x85490) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  FUN_00406b70(local_2c);
  FUN_00406b98(param_1 + 0x855ac);
  *(undefined1 **)(param_1 + 0x855b0) = &DAT_004a25a0;
  InterlockedIncrement(&DAT_004a2590);
  *(undefined4 *)(param_1 + 0x855b4) = param_2;
  *param_1 = 0;
  *(undefined4 *)(param_1 + 0x40) = 1;
  uVar1 = FUN_004836cc(4);
  *(undefined4 *)(param_1 + 0x33e64) = uVar1;
  uVar1 = FUN_004836cc(4);
  *(undefined4 *)(param_1 + 0x33e68) = uVar1;
  uVar1 = FUN_004836cc(4);
  *(undefined4 *)(param_1 + 0x33e6c) = uVar1;
  uVar1 = FUN_004836cc(4);
  *(undefined4 *)(param_1 + 0x33e70) = uVar1;
  uVar1 = FUN_004836cc(4);
  *(undefined4 *)(param_1 + 0x85484) = uVar1;
  uVar1 = FUN_004836cc(4);
  *(undefined4 *)(param_1 + 0x85488) = uVar1;
  uVar1 = FUN_004836cc(0x100);
  *(undefined4 *)(param_1 + 0x3447c) = uVar1;
  uVar1 = FUN_004836cc(0x100);
  *(undefined4 *)(param_1 + 0x34480) = uVar1;
  uVar1 = FUN_004836cc(4);
  **(undefined4 **)(param_1 + 0x33e6c) = uVar1;
  uVar1 = FUN_004836cc(4);
  **(undefined4 **)(param_1 + 0x33e70) = uVar1;
  uVar1 = FUN_004836cc(1);
  **(undefined4 **)(param_1 + 0x85484) = uVar1;
  uVar1 = FUN_004836cc(1);
  **(undefined4 **)(param_1 + 0x85488) = uVar1;
  iVar3 = 0;
  do {
    uVar1 = FUN_004836cc(4);
    *(undefined4 *)(*(int *)(param_1 + 0x3447c) + iVar3 * 4) = uVar1;
    piVar2 = (int *)FUN_004836cc(0xc);
    if (piVar2 != (int *)0x0) {
      FUN_00483a78(piVar2,8,1,0x211,FUN_0040d9dc);
    }
    *(int **)(*(int *)(param_1 + 0x34480) + iVar3 * 4) = piVar2;
    iVar3 = iVar3 + 1;
  } while (iVar3 < 0x40);
  FUN_00406b38((int)local_28,2);
  FUN_00406b38((int)local_20,2);
  FUN_00406b38((int)local_1c,2);
  FUN_00406b38((int)local_18,2);
  FUN_00406b38((int)local_14,2);
  FUN_00406b38((int)local_10,2);
  FUN_00406b38((int)local_c,2);
  FUN_00406b38((int)local_8,2);
  *in_FS_OFFSET = local_54;
  return param_1;
}


