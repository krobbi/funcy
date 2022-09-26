# Funcy Virtual Machine
_Specification for the Funcy Virtual Machine (FVM), a stack-based bytecode
interpreter for Funcy._  
__Format version `1`.__  
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
   * [JUMP (`0x02`)](#jump-0x02)
   * [JUMP_NOT_ZERO (`0x03`)](#jumpnotzero-0x03)
   * [JUMP_ZERO (`0x04`)](#jumpzero-0x04)
   * [CALL (`0x05`)](#call-0x05)
   * [RETURN (`0x06`)](#return-0x06)
   * [DROP (`0x07`)](#drop-0x07)
   * [DUPLICATE (`0x08`)](#duplicate-0x08)
   * [PUSH_U8 (`0x09`)](#pushu8-0x09)
   * [PUSH_S8 (`0x0a`)](#pushs8-0x0a)
   * [PUSH_U16 (`0x0b`)](#pushu16-0x0b)
   * [PUSH_S16 (`0x0c`)](#pushs16-0x0c)
   * [PUSH_U32 (`0x0d`)](#pushu32-0x0d)
   * [PUSH_S32 (`0x0e`)](#pushs32-0x0e)
   * [LOAD_LOCAL (`0x0f`)](#loadlocal-0x0f)
   * [STORE_LOCAL (`0x10`)](#storelocal-0x10)
   * [UNARY_NEGATE (`0x11`)](#unarynegate-0x11)
   * [UNARY_NOT (`0x12`)](#unarynot-0x12)
   * [BINARY_ADD (`0x13`)](#binaryadd-0x13)
   * [BINARY_SUBTRACT (`0x14`)](#binarysubtract-0x14)
   * [BINARY_MULTIPLY (`0x15`)](#binarymultiply-0x15)
   * [BINARY_DIVIDE (`0x16`)](#binarydivide-0x16)
   * [BINARY_MODULO (`0x17`)](#binarymodulo-0x17)
   * [BINARY_EQUALS (`0x18`)](#binaryequals-0x18)
   * [BINARY_NOT_EQUALS (`0x19`)](#binarynotequals-0x19)
   * [BINARY_GREATER (`0x1a`)](#binarygreater-0x1a)
   * [BINARY_GREATER_EQUALS (`0x1b`)](#binarygreaterequals-0x1b)
   * [BINARY_LESS (`0x1c`)](#binaryless-0x1c)
   * [BINARY_LESS_EQUALS (`0x1d`)](#binarylessequals-0x1d)
   * [BINARY_AND (`0x1e`)](#binaryand-0x1e)
   * [BINARY_OR (`0x1f`)](#binaryor-0x1f)
   * [PRINT (`0x20`)](#print-0x20)

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
version of FVM bytecode being used. Bytecode files store the following sequence
of data:

| Type        | Description                                                 |
| ----------: | :---------------------------------------------------------- |
| `u8`        | `0x83`: Ensures bit 7 is set. Function symbol in ANSI.      |
| `3 * u8`    | `0x46 0x56 0x4d`: `FVM` identifier.                         |
| `2 * u8`    | `0x0d 0x0a`: `\r\n`, tests for line ending conversion.      |
| `u8`        | `0x1a`: Stops file display on some systems.                 |
| `u8`        | `0x0a`: `\n`, tests for reverse line ending conversion.     |
| `u32`       | Format version. `0x01 0x00 0x00 0x00 (1)` for this version. |
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
* An element is popped from `sm` while it is empty.
* An element is accessed from out of bounds of `sm`.
* A modulo or divide by `0` operation is performed.

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

## JUMP (`0x02`)
1. Pop an element, `jumpAddress` from `sm`.
2. Set `ip` to `branchAddress`.

## JUMP_NOT_ZERO (`0x03`)
1. Pop an element `jumpAddress` from `sm`.
2. Pop an element `compareValue` from `sm`.
3. Set `ip` to `jumpAddress` if `compareValue` is not equal to `0`.

## JUMP_ZERO (`0x04`)
1. Pop an element `jumpAddress` from `sm`.
2. Pop an element `compareValue` from `sm`.
3. Set `ip` to `jumpAddress` if `compareValue` is equal to `0`.

## CALL (`0x05`)
1. Pop an element, `argCount` from `sm`.
2. Pop an element, `callAddress` from `sm`.
3. Pop the top `argCount` elements from `sm` in order as `args`.
4. Push the value of `fp` to `sm`.
5. Set `fp` to the top index of `sm`.
6. Push the value of `ip` to `sm`.
7. Set `ip` to `callAddress`.
8. Replace `args` at the top of `sm` in order.

## RETURN (`0x06`)
1. Read a value, `oldFP` from `fp`'s value.
2. Set `ip` to `sm[oldFP + 1]`.
3. Set `fp` to `sm[oldFP]`.
4. Pop an element, `returnValue` from `sm`.
5. Discard all elements from `sm` with an index greater than or equal to
`oldFP`.
6. Push `returnValue` to `sm`.

## DROP (`0x07`)
1. Pop and discard an element from `sm`.

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
1. Pop an element, `offset` from `sm`.
2. Push `sm[fp + offset]` to `sm`.

## STORE_LOCAL (`0x10`)
1. Pop an element, `offset` from `sm`.
2. Peek a value, `value` from the top of `sm`.
3. Set `sm[fp + offset]` to `value`.

## UNARY_NEGATE (`0x11`)
1. Pop an element, `value` from `sm`.
2. Push `-value` to `sm`.

## UNARY_NOT (`0x12`)
1. Pop an element, `value` from `sm`.
2. Push `int(value == 0)` to `sm`.

## BINARY_ADD (`0x13`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `x + y` to `sm`.

## BINARY_SUBTRACT (`0x14`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `x - y` to `sm`.

## BINARY_MULTIPLY (`0x15`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `x * y` to `sm`.

## BINARY_DIVIDE (`0x16`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `x // y` to `sm`.

## BINARY_MODULO (`0x17`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `x % y` to `sm`.

## BINARY_EQUALS (`0x18`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x == y)` to `sm`.

## BINARY_NOT_EQUALS (`0x19`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x != y)` to `sm`.

## BINARY_GREATER (`0x1a`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x > y)` to `sm`.

## BINARY_GREATER_EQUALS (`0x1b`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x >= y)` to `sm`.

## BINARY_LESS (`0x1c`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x < y)` to `sm`.

## BINARY_LESS_EQUALS (`0x1d`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x <= y)` to `sm`.

## BINARY_AND (`0x1e`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x != 0 and y != 0)` to `sm`.

## BINARY_OR (`0x1f`)
1. Pop an element, `y` from `sm`.
2. Pop an element, `x` from `sm`.
3. Push `int(x != 0 or y != 0)` to `sm`.

## PRINT (`0x20`)
1. Pop an element, `value` from `sm`.
2. Print `value` with a line break.
