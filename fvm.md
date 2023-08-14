# Funcy Virtual Machine
_Specification for the Funcy Virtual Machine (FVM), a stack-based bytecode
interpreter for Funcy._  
__Format version `2`.__  
__Copyright &copy; 2022-2023 Chris Roberts__ (Krobbizoid).

[Go back](./readme.md).

# Contents
1. [Architecture](#architecture)
2. [Data Types](#data-types)
3. [Bytecode Files](#bytecode-files)
4. [Execution](#execution)
5. [Opcodes](#opcodes)
   * [HALT (`0x00`)](#halt-0x00)
   * [NO_OPERATION (`0x01`)](#no_operation-0x01)
   * [JUMP (`0x02`)](#jump-0x02)
   * [JUMP_NOT_ZERO (`0x03`)](#jump_not_zero-0x03)
   * [JUMP_ZERO (`0x04`)](#jump_zero-0x04)
   * [CALL (`0x05`)](#call-0x05)
   * [RETURN (`0x06`)](#return-0x06)
   * [DROP (`0x07`)](#drop-0x07)
   * [DUPLICATE (`0x08`)](#duplicate-0x08)
   * [PUSH_U8 (`0x09`)](#push_u8-0x09)
   * [PUSH_S8 (`0x0a`)](#push_s8-0x0a)
   * [PUSH_U16 (`0x0b`)](#push_u16-0x0b)
   * [PUSH_S16 (`0x0c`)](#push_s16-0x0c)
   * [PUSH_U32 (`0x0d`)](#push_u32-0x0d)
   * [PUSH_S32 (`0x0e`)](#push_s32-0x0e)
   * [LOAD_LOCAL (`0x0f`)](#load_local-0x0f)
   * [STORE_LOCAL (`0x10`)](#store_local-0x10)
   * [UNARY_DEREFERENCE (`0x11`)](#unary_dereference-0x11)
   * [UNARY_NEGATE (`0x12`)](#unary_negate-0x12)
   * [UNARY_NOT (`0x13`)](#unary_not-0x13)
   * [BINARY_ADD (`0x14`)](#binary_add-0x14)
   * [BINARY_SUBTRACT (`0x15`)](#binary_subtract-0x15)
   * [BINARY_MULTIPLY (`0x16`)](#binary_multiply-0x16)
   * [BINARY_DIVIDE (`0x17`)](#binary_divide-0x17)
   * [BINARY_MODULO (`0x18`)](#binary_modulo-0x18)
   * [BINARY_EQUALS (`0x19`)](#binary_equals-0x19)
   * [BINARY_NOT_EQUALS (`0x1a`)](#binary_not_equals-0x1a)
   * [BINARY_GREATER (`0x1b`)](#binary_greater-0x1b)
   * [BINARY_GREATER_EQUALS (`0x1c`)](#binary_greater_equals-0x1c)
   * [BINARY_LESS (`0x1d`)](#binary_less-0x1d)
   * [BINARY_LESS_EQUALS (`0x1e`)](#binary_less_equals-0x1e)
   * [BINARY_AND (`0x1f`)](#binary_and-0x1f)
   * [BINARY_OR (`0x20`)](#binary_or-0x20)
   * [PUT_CHR (`0x21`)](#put_chr-0x21)

# Architecture
The FVM uses several regions of memory to execute FVM bytecode:

* Program memory, or `pm` is a read-only array of bytes that stores FVM
bytecode and program data. The size of `pm` may be variable, but it should be
at least the size of the currently executed program. The program must originate
at index `0`.
* The instruction pointer, or `ip` is an integer that stores an index of `pm`.
It is used for fetching FVM opcodes and program data.
* Stack memory, or `sm` is a stack of signed integer words that stores locals
and the inputs and outputs of most operations. The size of a stack word is
undefined, but 32 bits is recommended. There is no defined limit for the size
of `sm`. The index of the top word of `sm` increases as words are pushed to it.
* The frame pointer, or `fp` is an integer that stores an index of `sm` and
defines the base of the current call frame. `fp` stores the index of a word in
`sm`, _not_ a byte. Offsets from `fp` in `sm` are used to access locals.
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
version of FVM bytecode being used. Bytecode files store the following sequence
of data:

| Type        | Description                                                 |
| ----------: | :---------------------------------------------------------- |
| `u8`        | `0x83`: Ensures bit 7 is set. Function symbol in ANSI.      |
| `3 * u8`    | `0x46 0x56 0x4d`: `FVM` identifier.                         |
| `2 * u8`    | `0x0d 0x0a`: `\r\n`, tests for line ending conversion.      |
| `u8`        | `0x1a`: Stops file display on some systems.                 |
| `u8`        | `0x0a`: `\n`, tests for reverse line ending conversion.     |
| `u32`       | Format version. `0x02 0x00 0x00 0x00 (2)` for this version. |
| `u32`       | `size` value. The number of bytes of FVM bytecode.          |
| `size * u8` | The FVM bytecode to load into `pm`.                         |

Any trailing data is unused and has no effect. If the bytecode file is too
small for the `size` value it will fail to load.

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
* A word is popped from `sm` while it is empty.
* A word is accessed from out of bounds of `sm`.
* A modulo or divide by `0` operation is performed.

# Opcodes
An opcode is a `u8` value in FVM bytecode that represents an operation. Each
opcode executes a sequence of operations. Opcodes have defined values, but may
change between format versions:

## HALT (`0x00`)
1. Pop a word, `exitCode` from `sm`.
2. Set `ec` to `exitCode`.
3. Set `ef` to `false`.

## NO_OPERATION (`0x01`)
1. Do nothing.

## JUMP (`0x02`)
1. Pop a word, `jumpAddress` from `sm`.
2. Set `ip` to `branchAddress`.

## JUMP_NOT_ZERO (`0x03`)
1. Pop a word `jumpAddress` from `sm`.
2. Pop a word `compareValue` from `sm`.
3. Set `ip` to `jumpAddress` if `compareValue` is not equal to `0`.

## JUMP_ZERO (`0x04`)
1. Pop a word `jumpAddress` from `sm`.
2. Pop a word `compareValue` from `sm`.
3. Set `ip` to `jumpAddress` if `compareValue` is equal to `0`.

## CALL (`0x05`)
1. Pop a word, `argCount` from `sm`.
2. Pop a word, `callAddress` from `sm`.
3. Pop the top `argCount` words from `sm` in order as `args`.
4. Push the value of `fp` to `sm`.
5. Set `fp` to the top index of `sm`.
6. Push the value of `ip` to `sm`.
7. Set `ip` to `callAddress`.
8. Replace `args` at the top of `sm` in order.

## RETURN (`0x06`)
1. Read a value, `oldFP` from `fp`'s value.
2. Set `ip` to `sm[oldFP + 1]`.
3. Set `fp` to `sm[oldFP]`.
4. Pop a word, `returnValue` from `sm`.
5. Discard all words from `sm` with an index greater than or equal to `oldFP`.
6. Push `returnValue` to `sm`.

## DROP (`0x07`)
1. Pop and discard a word from `sm`.

## DUPLICATE (`0x08`)
1. Peek a value, `value` from the top of `sm`.
2. Push `value` to `sm`.

## PUSH_U8 (`0x09`)
1. Fetch a `u8` value.
2. Push the value to `sm`.

## PUSH_S8 (`0x0a`)
1. Fetch an `s8` value.
2. Push the value to `sm`.

## PUSH_U16 (`0x0b`)
1. Fetch a `u16` value.
2. Push the value to `sm`.

## PUSH_S16 (`0x0c`)
1. Fetch an `s16` value.
2. Push the value to `sm`.

## PUSH_U32 (`0x0d`)
1. Fetch a `u32` value.
2. Push the value to `sm`.

## PUSH_S32 (`0x0e`)
1. Fetch an `s32` value.
2. Push the value to `sm`.

## LOAD_LOCAL (`0x0f`)
1. Pop a word, `offset` from `sm`.
2. Push `sm[fp + offset]` to `sm`.

## STORE_LOCAL (`0x10`)
1. Pop a word, `offset` from `sm`.
2. Peek a value, `value` from the top of `sm`.
3. Set `sm[fp + offset]` to `value`.

## UNARY_DEREFERENCE (`0x11`)
1. Pop a word, `address` from `sm`.
2. Push `pm[address]` to `sm`.

## UNARY_NEGATE (`0x12`)
1. Pop a word, `value` from `sm`.
2. Push `-value` to `sm`.

## UNARY_NOT (`0x13`)
1. Pop a word, `value` from `sm`.
2. Push `int(value == 0)` to `sm`.

## BINARY_ADD (`0x14`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `x + y` to `sm`.

## BINARY_SUBTRACT (`0x15`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `x - y` to `sm`.

## BINARY_MULTIPLY (`0x16`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `x * y` to `sm`.

## BINARY_DIVIDE (`0x17`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `x // y` to `sm`.

## BINARY_MODULO (`0x18`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `x % y` to `sm`.

## BINARY_EQUALS (`0x19`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x == y)` to `sm`.

## BINARY_NOT_EQUALS (`0x1a`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x != y)` to `sm`.

## BINARY_GREATER (`0x1b`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x > y)` to `sm`.

## BINARY_GREATER_EQUALS (`0x1c`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x >= y)` to `sm`.

## BINARY_LESS (`0x1d`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x < y)` to `sm`.

## BINARY_LESS_EQUALS (`0x1e`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x <= y)` to `sm`.

## BINARY_AND (`0x1f`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x != 0 and y != 0)` to `sm`.

## BINARY_OR (`0x20`)
1. Pop a word, `y` from `sm`.
2. Pop a word, `x` from `sm`.
3. Push `int(x != 0 or y != 0)` to `sm`.

## PUT_CHR (`0x21`)
1. Peek a value, `value` from the top of `sm`.
2. Put the character with the value `value` to standard output.
