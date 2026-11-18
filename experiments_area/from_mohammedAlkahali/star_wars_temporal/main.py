# A tiny script to prove we can reach SWAPI (the Star Wars API) before we add
# Temporal on top. If this fails, the problem is the network or SWAPI, not
# our Temporal code, which makes debugging much easier later.

import httpx


def fetch_json(url: str) -> dict:
    # timeout=10: without a timeout a slow server could make us wait forever.
    response = httpx.get(url, timeout=10)
    # raise_for_status() turns 4xx/5xx answers into an exception, so we never
    # silently treat an error page as real data.
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # People #1 is Luke Skywalker, a quick and well-known test record.
    print(fetch_json("https://swapi.dev/api/people/1/"))
