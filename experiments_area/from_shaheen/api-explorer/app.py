import requests  # type: ignore[import-untyped]


def main():
    currancy = input("Enter currancy here: ").upper()

    try:
        respone = requests.get("https://open.er-api.com/v6/latest/" + currancy)
        result_dict = respone.json()

        data = [(currancy, result_dict["rates"][currancy])]

        converted_currancy = input(
            "Enter the currancy you want to convert too: "
        ).upper()

        data.append((converted_currancy, result_dict["rates"][converted_currancy]))

        final_output = f"The converted currancy: {data[0]}. converted to {data[1]}"

        print(final_output)
    except KeyError:
        print("You have entered invalid currancy!!")


if __name__ == "__main__":
    main()
