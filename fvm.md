# Funcy Virtual Machine
_Specification for the Funcy Virtual Machine (FVM), a stack-based bytecode
interpreter for Funcy._  
__Format version `0`.__  
__Copyright &copy; 2022 Chris Roberts__ (Krobbizoid).

[Go back](./readme.md).

# Contents
1. [Architecture](#architecture)
2. [Data Types](#data-types)
3. [Bytecode Files](#bytecode-files)
4. [Execution](#execution)
5. [Opcodes](#opcodes)
   * [HALT (`0x00`)](#halt-0x00)
   * [NO_OPERATION (`0x01`)](#nooperation-0x01)
   * [BRANCH_ALWAYS (`0x02`)](#branchalways-0x02)
   * [CALL (`0x03`)](#call-0x03)
   * [RETURN (`0x04`)](#return-0x04)
   * [PUSH_U8 (`0x05`)](#pushu8-0x05)
   * [PUSH_S8 (`0x06`)](#pushs8-0x06)
   * [PUSH_U16 (`0x07`)](#pushu16-0x07)
   * [PUSH_S16 (`0x08`)](#pushs16-0x08)
   * [PUSH_U32 (`0x09`)](#pushu32-0x09)
   * [PUSH_S32 (`0x0a`)](#pushs32-0x0a)
   * [DISCARD (`0x0b`)](#discard-0x0b)
   * [PRINT (`0x0c`)](#print-0x0c)

# Architecture
The FVM uses several regions of memory to execute FVM bytecode:

* Program memory, or `pm` is a read-only array of bytes that stores FVM
bytecode and program data. The size of `pm` may be variable, but it should be
at least the size of the currently executed program. The program must originate
at index `0`.
* The instruction pointer, or `ip` is an integer that stores an index of `pm`.
It is used for fetching FVM opcodes and program data.
* Stack memory, or `sm` is a stack of variable-type stack elements that stores
local variables and the inputs and outputs of most operations. Although `sm`
should support variable type elements, currently only signed integers are used.
There is no defined limit for the size of `sm`. The index of the top element of
`sm` increases as elements are pushed to it.
* The frame pointer, or `fp` is an integer that stores an index of `sm` and
defines the base of the current call frame. Offsets from `fp` in `sm` are used
to access local variables.
* The execution flag, or `ef` is a boolean value that stores whether the FVM is
executing a program.
* The exit code, or `ec` is an integer that stores an exit code for when
execution stops.

# Data Types
A fetch is a fundamental operation of the FVM that is used to read data from
`pm`. There are several types of data named by this specification:

| Name  | Size    | Description                                             |
| ----: | ------: | :------------------------------------------------------ |
| `u8`  | 1 byte  | An 8-bit unsigned integer. The type of FVM opcodes.     |
| `s8`  | 1 byte  | An 8-bit two's complement-signed integer.               |
| `u16` | 2 bytes | A 16-bit little-endian unsigned integer.                |
| `s16` | 2 bytes | A 16-bit little-endian two's complement-signed integer. |
| `u32` | 4 bytes | A 32-bit little-endian unsigned integer.                |
| `s32` | 4 bytes | A 32-bit little-endian two's complement-signed integer. |

To fetch data, the byte at `pm[ip]` is read. `ip` is then incremented. This is
repeated until the required number of bytes have been read. The result of this
is that `ip` will point to the byte immediately after the fetched data.

# Bytecode Files
To store FVM bytecode in a file, a header is included to identify the file as
FVM bytecode, ensure the file is being read as binary data, and identify the
version of FVM bytecode being used. The initial 8 bytes of the header are based
on the PNG format:

| Type        | Description                                                      |
| ----------: | :--------------------------------------------------------------- |
| `u8`        | `0x83`: Ensures bit 7 is set. Function symbol in ANSI.           |
| `3 * u8`    | `0x46 0x56 0x4D`: `FVM` identifier.                              |
| `2 * u8`    | `0x0d 0x0a`: `\r\n` sequence, tests for line ending conversion.  |
| `u8`        | `0x1a`: Stops file display on some systems.                      |
| `u8`        | `0x0a`: `\n`, tests for reverse line ending conversion.          |
| `u8`        | Architecture word size, currently unused and always `0x20 (32)`. |
| `u32`       | Format version. `0x00000000 (0)` for this specification.         |
| `u32`       | `size` value. The number of bytes of FVM bytecode.               |
| `size * u8` | The FVM bytecode to load into `pm`.                              |

Any trailing data is unused and has no effect.

Any file extension may be used for FVM bytecode files, but `.fyc` is
recommended for compiled Funcy code. The file extension `.fvm` is recommended
for other uses that target the FVM.

# Execution
The following sequence is used to execute a program. The FVM should only begin
executing a program if `ef` is `false`:

1. The program is loaded into `pm` starting at index `0`. Header data from
bytecode files is excluded.
2. `ip` is set to `0`.
3. `sm` is cleared.
4. `fp` is set to `0`.
5. `ec` is set to `0`.
6. `ef` is set to `true`.

Then, the FVM steps through 0 or more of the following cycles until `ef` is
`false`:

1. Fetch a `u8` opcode.
2. Execute the opcode. See [Opcodes](#opcodes) for details.

When execution finishes, the value of `ec` may be used as an exit code.

There are several illegal states that may be encountered during execution.
These are undefined and depend on the FVM's implementation:

* Data is fetched from out of bounds of `pm`.
* An undefined opcode is fetched.
* `sm` grows to an unsupported size.
* An element is popped from `sm` while it is empty.
* An element is accessed from out of bounds of `sm`.

# Opcodes
An opcode is a `u8` value in FVM bytecode that represents an operation. Each
opcode executes a sequence of operations. Opcodes have defined values, but may
change between format versions:

## HALT (`0x00`)
1. Pop an element, `exitCode` from `sm`.
2. Set `ec` to `exitCode`.
3. Set `ef` to `false`.

## NO_OPERATION (`0x01`)
1. Do nothing.

## BRANCH_ALWAYS (`0x02`)
1. Pop an element, `branchAddress` from `sm`.
2. Set `ip` to `branchAddress`.

## CALL (`0x03`)
1. Pop an element, `argCount` from `sm`.
2. Pop an element, `callAddress` from `sm`.
3. Pop the top `argCount` elements from `sm` in order as `args`.
4. Push the value of `fp` to `sm`.
5. Set `fp` to the top index of `sm`.
6. Push the value of `ip` to `sm`.
7. Set `ip` to `callAddress`.
8. Replace `args` at the top of `sm` in order.

## RETURN (`0x04`)
1. Pop an element, `returnValue` from `sm`.
2. Read an element, `poppedFP` from `sm[fp]`.
3. Set `ip` to `sm[fp + 1]`.
4. Set `fp` to `sm[fp]`.
5. Discard all elements from `sm` with an index greater than or equal to
`poppedFP`.
6. Push `returnValue` to `sm`.

## PUSH_U8 (`0x05`)
1. Fetch a `u8` value.
2. Push the value to `sm`.

## PUSH_S8 (`0x06`)
1. Fetch an `s8` value.
2. Push the value to `sm`.

## PUSH_U16 (`0x07`)
1. Fetch a `u16` value.
2. Push the value to `sm`.

## PUSH_S16 (`0x08`)
1. Fetch an `s16` value.
2. Push the value to `sm`.

## PUSH_U32 (`0x09`)
1. Fetch a `u32` value.
2. Push the value to `sm`.

## PUSH_S32 (`0x0a`)
1. Fetch an `s32` value.
2. Push the value to `sm`.

## DISCARD (`0x0b`)
1. Pop and discard an element from `sm`.

## PRINT (`0x0c`)
1. Pop an element, `value` from `sm`.
2. Print `value` with a line break.
