"""
Use this file to implement your solution for exercise 5-1 b.
"""
from fuzzingbook.Fuzzer import RandomFuzzer
from exercise_2a import FunctionCoverageRunner
import html


class RandomCoverageFuzzer(RandomFuzzer):
    
    def runs(self, runner: FunctionCoverageRunner):
        
        # Run `runner` with fuzz input until `max_consecutive_failures` consecutive failures

        Covrage = set()
        result = []
        max_consecutive_failures = 10
        consecutive_failures = 0

        while consecutive_failures < max_consecutive_failures:

            iteration_result = self.run(runner)
            iteration_coverage = runner.covrage
            result.append(iteration_result)

            if iteration_coverage > Covrage:
                consecutive_failures = 0
                Covrage |= iteration_coverage
            else:
                consecutive_failures += 1

        return result

if __name__ == '__main__':
    fuzzer = RandomCoverageFuzzer()
    print(fuzzer.runs(FunctionCoverageRunner(html.escape)))
