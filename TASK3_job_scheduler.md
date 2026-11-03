# Task 3 (Hard): Job Scheduler

**File name:** `scheduler.py`

---

## The idea: think of a kitchen 🍳

You are cooking dinner with **2 cooks**. There are 4 jobs:

| Job | Takes | Can start only after... |
|---|---|---|
| cut vegetables | 5 min | (nothing, can start right away) |
| boil rice | 8 min | (nothing) |
| make curry | 6 min | cut vegetables is finished |
| serve | 2 min | boil rice **and** make curry are finished |

What happens:
```
minute 0:   cook 1 starts "boil rice"         cook 2 starts "cut vegetables"
minute 5:                                      cook 2 finishes "cut vegetables"
                                               cook 2 starts "make curry"
minute 8:   cook 1 finishes "boil rice"       (cook 1 waits: "serve" still needs the curry)
minute 11:                                     cook 2 finishes "make curry"
            cook 1 starts "serve"
minute 13:  cook 1 finishes "serve"   → dinner is ready in 13 minutes
```

Your program does exactly this, but for **any list of jobs** and **any number of workers**.
Computers do this all the time, for example when building software (first compile, then test,
then package, then deploy).

---

## How to run it

```
python scheduler.py jobs.txt --workers 2
```

- `jobs.txt`: the file with the jobs
- `--workers 2`: how many workers (cooks) there are. Must be a whole number of 1 or more.

---

## The jobs file

One job per line:                                                                
```
job <name> time=<minutes> needs=<job1>,<job2> retries=<number> fails=<number>
```

| Part | Meaning | Required? |
|---|---|---|
| `job <name>` | the line starts with the word `job`, then the job name (letters, digits, `_` and `-` only) | yes |
| `time=5` | how long the job takes (whole number, 1 or more) | yes |
| `needs=a,b` | the jobs that must be **finished** before this one can start (comma, no spaces) | no (default: nothing) |
| `retries=2` | if the job fails, how many times it may **try again** | no (default: 0) |
| `fails=1` | **for testing only:** pretend the first N attempts fail | no (default: 0) |

- The parts after the name can be in **any order**: `job b needs=a time=2` is fine.
- Extra spaces are fine. **Empty lines** and lines starting with **`#`** (comments) are ignored.

The kitchen as a file (`kitchen.txt` in this folder):
```
# Making dinner. One line = one job.
job cut_vegetables time=5
job boil_rice      time=8
job make_curry     time=6  needs=cut_vegetables
job serve          time=2  needs=boil_rice,make_curry
```

---

## The rules of the simulation

Time starts at **t=0**. Workers are numbered **worker1, worker2, ...**

### Which job starts?
A job is **ready** when everything in its `needs` is finished (DONE).
Whenever a worker is free and there are ready jobs:
1. The **longest job goes first** (biggest `time`).
2. If two jobs take the same time → **alphabetical order** by name (`alpha` before `beta`).
3. The job goes to the free worker with the **lowest number** (worker1 before worker2).

### What happens at the same moment?
At each moment in time, in this order:
1. **First**, jobs that end now finish (in worker order: worker1 first). Print DONE / FAIL.
2. **Then** the jobs that must be skipped are skipped (see failures). Print SKIP.
3. **Then** free workers start new jobs. Print START.

So a worker that finishes at t=5 can start a new job at t=5.

### Failures and retries
A job can fail (in this task, it fails because of `fails=`). For example, `fails=1` means the
**1st attempt fails** and the 2nd attempt works.
- The job has **1 + retries** attempts in total. `retries=2` → up to 3 attempts.
- An attempt takes the full `time`, even when it fails.
- After a failed attempt **with attempts left**: the job becomes ready again **straight away**
  and follows the same rules as all other ready jobs (longest first...).
- After the **last** attempt fails: the job is **FAILED**.
  Every job that needs it is **SKIPPED**: also jobs that need a skipped job, and so on
  (if A failed, B needs A, and C needs B → B and C are both skipped).
  Skipped jobs never start.
  **Jobs that don't depend on the failed job keep running normally.**

### The end
The simulation ends when no job is running and nothing more can start.

---

## The output (print exactly this format)

One line per event:
```
t=<time> worker<number> START <job>
t=<time> worker<number> DONE <job>
t=<time> worker<number> FAIL <job> (attempt <n> of <total attempts>)
t=<time> SKIP <job>
```
- Events are printed in time order, and at the same time in the order explained above
  (DONE/FAIL → SKIP → START).
- Several SKIPs at the same moment → alphabetical order.

Then a summary (lists in **alphabetical order**, `-` if the list is empty):
```
TOTAL TIME: <time when the last job ended>
DONE: <job>, <job>, ...
FAILED: <job>, ...
SKIPPED: <job>, ...
```

---

## Errors (check the whole file BEFORE running anything)

Print the message and exit with code 1. The line number is the real line in the file
(the first line is line 1, and comments and empty lines count too).

| Problem | Print |
|---|---|
| A line doesn't start with `job`, has no name, the name has bad characters, or a part has no `=` | `ERROR: line 3: bad line` |
| An unknown part, e.g. `colour=red` | `ERROR: line 3: unknown field colour` |
| `time` missing, not a whole number, or less than 1 | `ERROR: line 3: invalid time` |
| `retries` not a whole number of 0 or more | `ERROR: line 3: invalid retries` |
| `fails` not a whole number of 0 or more | `ERROR: line 3: invalid fails` |
| Two jobs with the same name | `ERROR: line 5: duplicate job compile` (the line of the 2nd one) |
| No jobs in the file | `ERROR: no jobs` |
| `needs` names a job that doesn't exist | `ERROR: job package needs unknown job tests` |
| **Circular dependency** (see below) | `ERROR: circular dependency: b -> c -> b` |
| Bad `--workers` (`0`, `-1`, `two`, `1.5`) | `ERROR: workers must be a whole number 1 or more` |
| The file doesn't exist | `ERROR: file not found: <file name>` |

Check the lines from top to bottom and stop at the **first** error. Check unknown needs **after**
reading all lines (a job may need a job that is written further down).

### Circular dependency: an impossible plan
```
job a time=1 needs=b
job b time=1 needs=c
job c time=1 needs=b
```
`b` waits for `c`, and `c` waits for `b`. They would wait forever! Your program must find this and
print the **loop**:
```
ERROR: circular dependency: b -> c -> b
```
**How to find the loop so the answer is always the same:** start with the jobs in the order they
are written in the file. From each job, follow its `needs` in the order they are written, going
deeper and deeper (this is called "depth-first search"; search "python depth first search
cycle detection"). The first time you arrive at a job that is **already on the path you are
walking**, the loop is from that job back to itself.

In the example: start at `a` → go to `b` → go to `c` → `c` needs `b`, and **`b` is already on my
path** (a → b → c). So the loop is `b -> c -> b`.

More examples:
- `job a time=1 needs=a` → `a -> a`
- `a` needs `b`, `b` needs `a` → `a -> b -> a`

---

## Examples (all files are in this folder)

### Example 1: the kitchen with 2 workers
`python scheduler.py kitchen.txt --workers 2` (also in `expected_kitchen_2workers.txt`):
```
t=0 worker1 START boil_rice
t=0 worker2 START cut_vegetables
t=5 worker2 DONE cut_vegetables
t=5 worker2 START make_curry
t=8 worker1 DONE boil_rice
t=11 worker2 DONE make_curry
t=11 worker1 START serve
t=13 worker1 DONE serve
TOTAL TIME: 13
DONE: boil_rice, cut_vegetables, make_curry, serve
FAILED: -
SKIPPED: -
```
Why does `boil_rice` get worker1? Both jobs are ready at t=0. `boil_rice` (8) is longer than
`cut_vegetables` (5), so it goes first, to the lowest worker. Why does `serve` go to worker1 at
t=11? Both workers are free then, and worker1 is the lowest number.

### Example 2: the kitchen with only 1 worker
`--workers 1` → `expected_kitchen_1workers.txt` (total time 21: one cook does everything in turn).

### Example 3: a job that fails once and then works (`pipeline.txt`)
```
job compile  time=5
job lint     time=2
job test     time=8  needs=compile
job package  time=3  needs=test,lint
job deploy   time=4  needs=package  retries=2 fails=1
job docs     time=1
```
`--workers 2` → `expected_pipeline_2workers.txt`. The important part:
```
t=16 worker1 START deploy
t=20 worker1 FAIL deploy (attempt 1 of 3)
t=20 worker1 START deploy
t=24 worker1 DONE deploy
TOTAL TIME: 24
```

### Example 4: a job that fails for good (`broken.txt`)
```
job download time=3
job install  time=4  needs=download  retries=1 fails=5
job setup    time=2  needs=install
job report   time=1  needs=setup
job clean    time=6
```
`--workers 2` → `expected_broken_2workers.txt`:
```
t=0 worker1 START clean
t=0 worker2 START download
t=3 worker2 DONE download
t=3 worker2 START install
t=6 worker1 DONE clean
t=7 worker2 FAIL install (attempt 1 of 2)
t=7 worker1 START install
t=11 worker1 FAIL install (attempt 2 of 2)
t=11 SKIP report
t=11 SKIP setup
TOTAL TIME: 11
DONE: clean, download
FAILED: install
SKIPPED: report, setup
```
`install` had 2 attempts (1 + `retries=1`) and both failed. `setup` needs `install` → skipped.
`report` needs `setup` → also skipped. `clean` doesn't need anything that failed, so it finished
normally. At t=7 the retry went to **worker1** because both workers were free and worker1 is the
lowest number.

### Example 5: the impossible plan (`loop.txt`)
```
ERROR: circular dependency: b -> c -> b
```

---

## Python you will use
- **Reading and splitting text** (`str.split`, `str.partition`)
- **Dictionaries** (name → job) and **classes / dataclasses** (one `Job`)
- **Sorting with a key**: e.g. `sorted(jobs, key=lambda j: (-j.time, j.name))`
- **Recursion** for finding loops (depth-first search)
- **A simulation loop**: jump from one "a job ends" moment to the next one

## Step-by-step guide (suggested)
1. Read the file, skip comments/empty lines, split each line into its parts. Print the jobs.
2. Add every file error from the table. Test each one.
3. Find circular dependencies. Test with all 3 loop examples above.
4. The simulation **without failures**: start jobs at t=0, find the next time a job ends, finish
   it, start new jobs, repeat. Get Example 1 and Example 2 exactly right.
5. Add failures and retries (Example 3).
6. Add SKIP for jobs that depend on failed jobs, including indirect ones (Example 4).
7. Print the summary.
8. Your tests in `tests/test_scheduler.py` (at least 12).

## Checklist before you submit
- [ ] All 5 examples give exactly the same output as the `expected_...txt` files
- [ ] Every error from the table works and nothing crashes
- [ ] Longest-first, alphabetical ties and lowest worker number are all correct
- [ ] Failed jobs skip everything that depends on them, even indirectly
- [ ] At least 12 tests, all passing
- [ ] Committed and pushed
