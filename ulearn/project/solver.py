from collections import namedtuple

TestResults = namedtuple("TestResults", ["success", "error"])

def get_solution() -> str:
    return "code"


def run_tests(solution: str) -> TestResults:
    i=0
    if i > 0:
        return TestResults(success=False, error=["biba_code", Exception()])
    else:
        return TestResults(success=True, error=(None, None))


def fix_solution(old_solution: str, error: tuple[str, Exception]) -> str:
    return f"{old_solution}\nfixed {error[0]}"


def solve() -> str:
    solution = get_solution()
    test_stat = run_tests(solution)

    while not test_stat.success:
        solution = fix_solution(solution, test_stat.error)
        test_stat = run_tests(solution)

    return solution

r = solve()
print(r)
