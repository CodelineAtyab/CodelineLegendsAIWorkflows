import asyncio
import time


async def count_to_five(label: str) -> list[int]:
  numbers: list[int] = []

  for count in range(1, 6):
    print(f"{label}: {count}")
    numbers.append(count)
    await asyncio.sleep(1)  # Let the other task run while this one waits.

  return numbers


async def main() -> None:
  results = await asyncio.gather(
    count_to_five("Task 1"),
    count_to_five("Task 2"),
  )

  print(f"Results are: {results}")


if __name__ == "__main__":
  start_time = time.perf_counter()
  asyncio.run(main())
  print(f"Time it took in seconds: {time.perf_counter() - start_time:.2f}")
