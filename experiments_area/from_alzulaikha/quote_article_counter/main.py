from quote import create_quotes_file, analyze_quotes


def main():
    create_quotes_file()

    with open("quotes_analysis.txt", "w"):
        pass

    analyze_quotes()


if __name__ == "__main__":
    main()
