Title: Notes from reading The Implementation of Lua 5.0
Author: David Wilemski
Category: blog
Slug: notes-from-the-implementation-of-lua
Date: 2018-03-28 23:15:00
Status: published
Tags: papers

Inspired by [a tweet from @munificentbob](https://twitter.com/munificentbob/status/974147769475547136)) I recently read this paper about Lua. I took some notes while reading and though I'd dump them here. Some of the implementation decisions and data structures were pretty interesting to me. These notes are pretty raw and only a little bit cleaned up from my handwritten shorthand.

Many things that were very interesting to me in the paper but these were some of the highlights (I have some notes on all of these below):

- The implementation of the associative array
- Upvalues
- Some of the optimizations in the byte code for making common Lua operations fast.
- The use of the C stack for tracking coroutine execution.

I don't have very much experience with building interpreters or compilers - an undergrad compilers class and a fair bit of reading about CPython implementation details - but still found this paper very readable. It touches on concepts at a high level and seems to have fairly good references for deeper reading if you want to learn more about a given topic. With all that said, here are the notes I took:


## Lua 5 vs Lua 4
- Register-based VM (instead of stack based).
- Lua does not have arrays, only tables (hash tables)
	- Lua 5 can recognize tables used as arrays and back these w/ an array for efficiency
- Implementation of closures: only copy to heap if stack-based locals go out of scope
- Addition of coroutines


## Lua Design/Implementation Goals
- Simplicity: both in language features and in terms of C code to implement
- Efficiency: fast compilation and execution of Lua programs
	- fast, smart, one-pass compiler and fast VM
- Portability: Clean warning free implementation that can run on as many platforms as possible
- Embeddability: designed to provide scripting facilities to larger programs
- Low Embedding Cost: easy and cheap to embed Lua.
- The compiler is 30% of the size of Lua core
	-  It is possible to embed Lua without the compiler and provide pre-compiled programs
- The scanner and parsers are hand written
	- smaller and more portable than yacc-generated code
		- used yacc until 3.0
- Compiler uses no IR
	- still performs some optimization (although the paper didn't cover this afaik)
- For portability, cannot use Direct Threaded code. See refs [8, 16]
	- Uses while-switch dispatch loop
	- Complicated implementation sometimes for portability

## Representation of Values
- Eight types: nil, boolean, number, string, table, function, user data, thread
	- Numbers are doubles
	- Strings are arrays of bytes with explicit sizes
	- Tables are associative arrays
	- Userdata: blocks of memory (pointers)
		- - light (memory managed by user) and heavy (garbage collection)
	- threads are coroutines
- Tagged union used to represent types
	- copying is expensive (3-4 words) because of this
- Needed for portability, can't use tricks that some languages (e.g. smalltalk) use to embed type info in spare bits.
	- (because byte alignment differences on various platforms)
- Doubles are not heap allocated for speed, would rather have copy cost

## Tables
- Assoc Arrays
- Indexable by any value (except Nil) and can store any value
- Can grow and shrink (when nil assigned to a key)
- No array type
- Tables are backed by both a hash table and by arrays
	- keys like strings end up in hash table 
	- Numeric keys from 1 onward are not stored, values stored in the array
- The backing array has a size limit N
	- goal for at least 1/2 of N to be used
	- "largest N such that at least half of the slots between 1 and N are in use and at least one used slot between N/2 + 1 and N"
	- Access to the array backed keys is faster because no hashing and takes half the memory (due to not storing keys).
	- Hash part is chained scatter table w/ Brent's Variation (Ref [3])
		- Another paper for me to read
		
## Functions and Closures
- Functions compiled into Prototypes containing vm instructions, constant values, and debug info.
- At runtime, any function...end expression creates a new closure.
- A closure has a reference to its Prototype, environment (e.g. global vars), and an array of references to Upvalues
	- Upvalues used to access outer local variables
- Function parameters in Lua are local variables
### Upvalues
- Any outer local value is accessed indirectly though an Upvalue
- Originally points to the stack slot where the variable lives.
- When the variable goes out of scope, it migrates into a slot in the up value itself
	- (So a copy is only incurred when needed)
- Mutable state is shared correctly among closures by creating at most one Upvalue per variable and reusing it across closures as needed.
- To ensure uniqueness, a linked list is kept with all open Upvalues of a stack
- When a new closure is created, the runtime goes through all outer locals and sees if the variable is already an Upvalue in the linked list.
	- If found, reuse, otherwise create a new Upvalue.
- List search typically probes only a few nodes because the list contains at most one entry for each local variable that is used by a nested function.
	- Question: Why a linked list? Is the mutation and traversal here infrequent enough to avoid allocation and pointer indirection overhead? Why not normal array or some other structure?
- Once a closed Upvalue is no longer reference by any closure, it is eventually GCed.

## Threads and Coroutines
- Lua 5.0 implements asymmetric coroutines
- Three standard library functions: create, resume, yield
- The `create` function receives a main function and creates a new coroutine with that function. Returns a value of type `thread` that represents that coroutine.
- `resume` (re)starts execution, calling the main function that was provided.
- `yield` suspends execution and returns control to the call that resumed that coroutine.
- Each coroutine has its own (abstract) stack
- These features are equivalent to continuations and allow all the features that implies (cooperative multithreading, generators, backtracking). See ref [7].
- `resume`/`yield` correspond to recursive calls/returns of the Lua interpreter function, using the C stack to track the Lua stack for coroutines.
	- This implies the interpreter is able to run multiple times, recursively, within the same process without issue.
	- The closure implementation helps here by avoiding issues with locals going out of scope.

## The Virtual Machine
- Lua compiles programs into opcodes and then executes the opcodes.
- When Lua enters a function it preallocates an activation record large enough to hold function registers.
- Register based VM
- All local variables are allocated in registers making access to locals very efficient.
- Register based code avoids expensive push and pop operations.
- Two common problems with register-based machines are code size and decoding overhead:
	- Instructions have to specify operands so most instructions are larger than instructions on a stack based machine because of implicit operands.
	- The paper says instructions are typically 4 bytes vs 1-2 bytes of previous stack-based implementation but that many fewer instructions are emitted for common operations so code size isn't significantly larger.
	- There is overhead in decoding operands from register machine instructions compared to implicit operands of stack machines.
	- Due to machine alignment and efficient use of logical operations for decoding, this is still fairly cheap.
- 35 instructions in Lua's VM
	- Detailed discussions of these in refs [14, 22]
- Access to registers, constants, and Upvalues are all fast due to being stored in various arrays.
- Access to globals is via a Lua table, accused by pre-computed string hashes (strings are interned), so this is two levels of indirection.
- Instructions are 32 bits divided into three or four fields.
	- Operations are 6 bits, providing 64 possible opcodes
	- Field A is always 8 bits.
	- Fields B and C take 9 bits each or can be combined into an 18 bit field (Bx is unsigned or SBx is signed).
	- Most instructions use three address format, A is the register for the result, B and C point to the operands.
		- Operands are either a register or a constant.
		- This makes typical Lua operations (like attribute access) take only one instruction.
- Branching post a problem so the VM uses two instructions:
	- The branch instruction itself, and alum that should be done if the test succeeds.
	- The jump is skipped if it fails.
	- This jump is fetched and executed within the same dispatch cycle as the branch so it is something of a special case within the VM.
- Lua uses two parallel stacks for function calls:
	- One stack has one entry for each active function and stores the function, return address, and base index for the activation record.
	- The other is a large array of Lua values that keeps the activation records.
		- each activation record has all temporary values (params, locals)
