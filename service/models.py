from flywheel import Field, Model


class Data(Model):
    id = Field(data_type=str, hash_key=True)
    val1 = Field(data_type=str)
    val2 = Field(data_type=int)
    val3 = Field(data_type=str)
