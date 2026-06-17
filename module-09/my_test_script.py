from data_generator import SpaceStationGenerator, DataConfig
from ex0.space_station import SpaceStation
from pydantic import ValidationError


def run_valid_tests():
    print("\n🚀 TESTANDO DADOS VÁLIDOS\n")

    config = DataConfig()
    generator = SpaceStationGenerator(config)

    stations = generator.generate_station_data(10)

    for data in stations:
        try:
            station = SpaceStation(**data)
            print(f"OK -> {station.station_id}")
        except ValidationError as e:
            print("❌ ERRO INESPERADO (dados válidos falharam):")
            print(e)


def run_invalid_tests():
    print("\n🧪 TESTANDO VALIDAÇÃO (ERROS ESPERADOS)\n")

    invalid_data = [
        {
            "station_id": "TOOLONG123456",
            "name": "Test Station",
            "crew_size": 25,
            "power_level": 85.0,
            "oxygen_level": 92.0,
            "last_maintenance": "2024-01-15T10:30:00",
        },
        {
            "station_id": "TS",
            "name": "",
            "crew_size": 0,
            "power_level": -10.0,
            "oxygen_level": 150.0,
            "last_maintenance": "2024-01-15T10:30:00",
        }
    ]

    for i, data in enumerate(invalid_data):
        try:
            SpaceStation(**data)
            print(f"❌ Teste {i} falhou: deveria dar erro")
        except ValidationError as e:
            print(f"✅ Teste {i} passou (erro esperado)")
            print(e.errors())


if __name__ == "__main__":
    run_valid_tests()
    run_invalid_tests()