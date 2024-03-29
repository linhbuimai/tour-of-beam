"""
Sample csv file:

user16_AmaranthKoala,AmaranthKoala,18,1447719060000,2015-11-16 16:11:03.921
user10_AndroidGreenKoala,AndroidGreenKoala,2,1447719060000,2015-11-16 16:11:03.955
user9_AuburnCockatoo,AuburnCockatoo,5,1447719060000,2015-11-16 16:11:03.955
user1_AntiqueBrassPlatypus,AntiqueBrassPlatypus,7,1447719060000,2015-11-16 16:11:03.955
user9_BattleshipGreyPossum,BattleshipGreyPossum,14,1447719060000,2015-11-16 16:11:03.955
user1_AmaranthDingo,AmaranthDingo,14,1447719060000,2015-11-16 16:11:03.955

Requirements:

- Sum up player score by username
"""

import apache_beam as beam
from src.utils import Output


if __name__ == "__main__":
    csv_path = "gs://apache-beam-samples/game/small/gaming_data.csv"
    p = beam.Pipeline()

    raw_data = (
        p
        | "Read csv file" >> beam.io.ReadFromText(csv_path)
        | beam.combiners.Sample.FixedSizeGlobally(10)
        | beam.FlatMap(lambda line: line)
        | beam.Map(lambda item: (item.split(",")[1], int(item.split(",")[2])))
        | beam.CombinePerKey(sum)
        | Output()
    )

    p.run()
