from manual_analysis import *
import ssl
import certifi

# This restores the same behavior as before.
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    data = 'manually.csv'
    average_yearly_duration(data)
    # total_monthly_duration(data)
    # total_yearly_duration(data)
    # total_seasonal_duration(data)

if __name__ == "__main__":
    main()


