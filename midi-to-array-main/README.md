# midi-to-array
Convert midi to pitch and time arrays and reversely.

## Requirements

python >= 3.6

Install requirements:

```shell
pip install mido
pip install click
```

## Usage

Convert midi file to array

```shell
python midi_to_array.py --input midi_file.mid --output file_to_store_array
```

Convert array to midi

```shell
python midi_to_array.py --input file_to_store_array --output output_midi.mid
```

For more information, run

```shell
python midi_to_array.py --help
```

## Output format

Line 1: pitch array. R stands for rest.

```
R R C3 R G#2 R G#2 R G2 R G2 R ...
```

If ``--format integer`` is set, pitches are represented by integers, where 60 stands for C4.
If ``--no-rest`` is set, rests are removed by prolonging the previous note.

Line 2: duration array. The numbers are lengths relative to a whole note.

```
1.0104166666666667 16.21875 0.24479166666666666 0.005208333333333333 0.24479166666666666 0.005208333333333333 ...
```

Line 3 (optional): tempo in microseconds per beat.

```
500000
```

