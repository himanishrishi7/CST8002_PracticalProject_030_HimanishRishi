class MilkSample:
    def __init__(self, sample_type: str, type: str, start_date: str, stop_date: str,
                 station_name: str, province: str, sr90_activity: float,
                 sr90_error: float, sr90_activity_per_calcium: float):
        """
        Initialize a MilkSample object with data from the CSV file.
        
        Args:
            sample_type (str): Type of sample (e.g., "MILK")
            type (str): Type of milk (e.g., "WHOLE")
            start_date (str): Start date of sampling period
            stop_date (str): End date of sampling period
            station_name (str): Name of the sampling station
            province (str): Province where the sample was taken
            sr90_activity (float): Strontium-90 activity in Bq/L
            sr90_error (float): Error in Sr-90 activity measurement
            sr90_activity_per_calcium (float): Sr-90 activity per calcium ratio
        """
        self._sample_type = sample_type
        self._type = type
        self._start_date = start_date
        self._stop_date = stop_date
        self._station_name = station_name
        self._province = province
        self._sr90_activity = sr90_activity
        self._sr90_error = sr90_error
        self._sr90_activity_per_calcium = sr90_activity_per_calcium

    # Properties for sample_type
    @property
    def sample_type(self) -> str:
        return self._sample_type

    @sample_type.setter
    def sample_type(self, value: str):
        self._sample_type = value

    # Properties for type
    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    # Properties for start_date
    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, value: str):
        self._start_date = value

    # Properties for stop_date
    @property
    def stop_date(self) -> str:
        return self._stop_date

    @stop_date.setter
    def stop_date(self, value: str):
        self._stop_date = value

    # Properties for station_name
    @property
    def station_name(self) -> str:
        return self._station_name

    @station_name.setter
    def station_name(self, value: str):
        self._station_name = value

    # Properties for province
    @property
    def province(self) -> str:
        return self._province

    @province.setter
    def province(self, value: str):
        self._province = value

    # Properties for sr90_activity
    @property
    def sr90_activity(self) -> float:
        return self._sr90_activity

    @sr90_activity.setter
    def sr90_activity(self, value: float):
        self._sr90_activity = value

    # Properties for sr90_error
    @property
    def sr90_error(self) -> float:
        return self._sr90_error

    @sr90_error.setter
    def sr90_error(self, value: float):
        self._sr90_error = value

    # Properties for sr90_activity_per_calcium
    @property
    def sr90_activity_per_calcium(self) -> float:
        return self._sr90_activity_per_calcium

    @sr90_activity_per_calcium.setter
    def sr90_activity_per_calcium(self, value: float):
        self._sr90_activity_per_calcium = value

    def __str__(self) -> str:
        """Return a string representation of the MilkSample object."""
        return (f"MilkSample(sample_type='{self._sample_type}', "
                f"type='{self._type}', "
                f"start_date='{self._start_date}', "
                f"stop_date='{self._stop_date}', "
                f"station_name='{self._station_name}', "
                f"province='{self._province}', "
                f"sr90_activity={self._sr90_activity}, "
                f"sr90_error={self._sr90_error}, "
                f"sr90_activity_per_calcium={self._sr90_activity_per_calcium})") 