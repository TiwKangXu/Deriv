from src.pipeline import (
    SupportTriagePipeline
)


def main():

    pipeline = (
        SupportTriagePipeline()
    )

    pipeline.run()


if __name__ == "__main__":

    main()