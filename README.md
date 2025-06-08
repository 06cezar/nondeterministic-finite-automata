# nondeterministic-finite-automata

An NFA (Nondeterministic Finite Automaton) is a 5-tuple (Q, Σ, δ, q0, F), consisting of
- a finite set of states Q
- a finite set of input symbols called the alphabet Σ
- a transition function δ : Q × Σ<sub>ε</sub> → P(Q), where Σ<sub>ε</sub> = Σ ∪ {ε}, and P(Q) is the power set of Q
- an initial (or start) state q<sub>0</sub>∈Q
- a set of accepting (or final) states F⊆Q

---

# Table of Contents
- [Definition Format](#definition-format)
- [Example Definition](#example-definition)
- [Error Handling](#error-handling)
- [NFA Emulator](#nfa-emulator)
- [Folder Structure](#folder-structure)
- [Usage](#usage)

---

# Definition Format

Each NFA is defined in a `.nfa` or `.txt` file using the following clearly defined sections:

- `[States]` — all states
- `[Sigma]` — all input symbols
- `[Rules]` — transitions written as `state, symbol, destination`
- `[Start]` — initial state
- `[Accept]` — final states

Each section ends with `End`.

This format is **intentionally aligned** with the one used in [this DFA project](https://github.com/06cezar/deterministic-finite-automata#clearly-defined-sections), with a few key differences:

### Differences from DFA:

- support for epsilon transitions, which are crucial for nondeterminism. 'epsilon' and the greek symbol 'ε' behave the same (by the way, utf-8 corruption is checked, so ε will render properly (e.g., "Îµ" → "ε"))
> You can write epsilon as either epsilon or ε. Both are accepted and interchangeable.
- because of nondeterminism we don't have errors anymore for conflicting transitions. (No DuplicateRuleError!) For example:
  
  ```
  q1, 0, q2
  q1, 0, q1 # ✅ Allowed in NFA!
  /* the NFA will go with both options, kinda like threads / parallelism!
     (nondeterminism :D) */
  ```
### Comments

- Single-line comments: start with `#`
- Multi-line comments: wrap between `/* ... */`
- Comments may appear inside sections and will be ignored by the parser

---

# Example Definition

A simple NFA that accepts the language L = { w ∈ {0,1}* | |w| ≡ 0 mod 2 or |w| ≡ 0 mod 3 } (all strings that contain only 0s and 1s and have lenghts divisible by 2, or by 3, or by both), found in the `NFA Definition Files/NFAmod2mod3.txt` file.

```
[States]
q0
q1
q2
q3
q4
q5
q6
End

[Sigma]
0
1
End

[Rules]
q0, ε, q1 # q1 -> q3 loop for mod 2 
q0, epsilon, q2
q0, 0, q6
q0, 1, q6
q1, 0, q3 
q1, 1, q3 
q3, 1, q1 
q3, 0, q1 
q2, 0, q4 # q2 -> q4 -> q5 loop for mod 3
q2, 1, q4
q4, 0, q5 
q4, 1, q5
q5, 0, q2 
q5, 1, q2

End

[Start]
q0
End

[Accept]
q1
q2
End

```
---

## ⚠️ Error Handling

The NFA implementation uses custom exception classes to handle invalid input formats, missing components, and runtime issues in a clean and Pythonic way.

### Defined Exceptions

| Exception | Description |
|----------|-------------|
| `UndefinedStartStateError` | Raised when the `[Start]` section is missing or the specified start state is undefined |
| `UndefinedAcceptStatesError` | Raised when the `[Accept]` section is missing or empty |
| `UndefinedAlphabetError` | Raised when the `[Sigma]` section is missing or contains no symbols |
| `InvalidStateError` | Raised when a state referenced in `[Start]`, `[Accept]`, or `[Rules]` is not declared in `[States]` |
| `InvalidSymbolError` | Raised when a symbol used in a rule is not part of `[Sigma]` (excluding epsilon) |
| `EpsilonTransitionError` | Raised if the user explicitly includes `epsilon` or `ε` in the alphabet, which is forbidden |
| `InputStringError` | Raised when an input string contains characters not defined in the alphabet |

### Notes

- **No Duplicate Rule Error**: Unlike DFA, an NFA **allows** multiple transitions from the same state on the same symbol.
- Epsilon transitions (written as `epsilon` or `ε`) are automatically handled and **must not** appear in `[Sigma]`.
- If a state has no defined rule for a symbol, it is treated as a self-loop (no-op), **not an error**.

### Example Error Messages

```
UndefinedStartStateError: Start state is not defined
UndefinedAcceptStatesError: Accept state is not defined
UndefinedAlphabetError: Alphabet is not defined
InvalidStateError: Accept state q5 is not defined
InvalidStateError: Source state q99 is not defined in the states list for the NFA
InvalidSymbolError: Symbol X is not defined in the alphabet for the NFA
EpsilonTransitionError: Epsilon doesn't need to be defined in the alphabet for the NFA
InputStringError: Input string contains symbols not in the given alphabet of the NFA
```
## NFA Emulator

The NFA emulator consists of the `emulateNFA.py` script and the `NFA.py` module. It supports both interactive use and command-line execution. This script simulates a Nondeterministic Finite Automaton (NFA) with epsilon transitions.

It reads:
- an NFA definition file (e.g., `.nfa` or `.txt`)
- an input string file
- and simulates the NFA to determine acceptance, showing steps optionally

---

### ✅ Features

- Supports epsilon transitions (`ε` or `epsilon`)
- Allows multiple transitions per input symbol (nondeterminism)
- Verbose mode for step-by-step state tracking
- Detects and handles UTF-8 corruption (e.g., `Îµ` → `ε`)
- Accepts flexible separators in input strings

---

## 📁 Folder Structure

```
project/
│
├── NFA.py
├── emulateNFA.py
├── NFA Definition Files/
│   └── your_machine.nfa
├── Input Files/
    └── your_input.txt
```

- the script in its current state uses the python OS module and chdir function to dynamically move back and forth through directories - so it can avoid hardcoded file paths - and also be cross-platform friendly, as file paths may be different between operating systems
- On Linux/macOS, paths look like:
```
NFA Definition Files/your_automaton.nfa
```
- On Windows, paths look like:
```
NFA Definition Files\your_automaton.nfa
```

---

## 📦 Requirements

To run the NFA emulator successfully, ensure the following structure:

- All core Python scripts (`NFA.py`, `emulateNFA.py`) should be in the project root folder.
- NFA definitions should be placed inside the `NFA Definition Files/` subfolder.
- Input strings should be placed inside the `Input Files/` subfolder.
- You should run the script from the **project root directory** using the terminal or an IDE.

## ▶️ Usage

### 🔹 Option 1: Interactive Mode

```
python3 emulateNFA.py
```

You’ll be prompted for:

- **NFA definition file name** - from `NFA Definition Files/`
- **Input string file name** - from `Input Files/`
- **Verbosity level:**
  - `1` → print all intermediate steps taken by the NFA
  - `0` → only print final result: `Accepted` or `Rejected`
- **Separator used between input symbols:**
  - `SPACE` → separator is a space (`' '`)
  - `NOSEPARATOR` → no separator (e.g., `abba`)
  - or any custom string (e.g., `;`, `,`, `|`)

### Option 2: Run via CLI

```
python3 emulateNFA.py <nfa_filename> <input_filename> [verbosity] [separator]
```

- `<nfa_filename>`: file in `NFA Definition Files/`
- `<input_filename>`: file in `Input Files/`

- `[verbosity]`: *(Optional)*  
  Use `1` to print steps, `0` to print only the final result.  
  Default is `0` (only displays Accepted/Rejected).

- `[separator]`: *(Optional)*  
  Use:
  - `SPACE` for `' '`
  - `NOSEPARATOR` for no separator
  - Or any other string like `;`, `,`, `|`

> ⚠️ If your separator is a shell-special character like ;, &, |, etc., wrap it in single quotes (';') to prevent shell misinterpretation.
```
python3 emulateNFA.py NFAmod2mod3.txt nfaInput.txt 1 NoSeparator
```

## Custom exceptions 
Custom exceptions are raised for:

- Missing DFA/input files

- Not enough CLI arguments

- Invalid working directories
