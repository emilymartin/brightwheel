from interview import providers


def main():
    final = providers.get_provider_data()
    print(f"{final.head()}")
    print(f"{final.shape}")


if __name__ == '__main__':
    main()
