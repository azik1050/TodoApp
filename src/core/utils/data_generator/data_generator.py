from faker import Faker


class DataGenerator:
    faker = Faker()

    @staticmethod
    def get_guid() -> str:
        return DataGenerator.faker.uuid4()