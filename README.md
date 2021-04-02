# Music Theory

## Examples

Get notes for any of the configured scales
```
print(get_notes(scale=Scales.DORIAN, key=Notes.D, with_intervals=True))

>>> [D(1), tone(2), E(2), semitone(1), F(3), tone(2), G(4), tone(2), A(5), tone(2), B(6), semitone(1), C(7), tone(2), D(8/1)]
```

Get chords for major scale in any key
```
print(get_chords(key=Notes.C))

>>> [C([C, E, G]), Dm([D, F, A]), Em([E, G, B]), F([F, A, C]), G([G, B, D]), Am([A, C, E]), Bdim([B, D, F])] 
```

Note analysis
```
print(get_notes(scale=Scales.DORIAN, key=Notes.D, with_intervals=True, octaves=2, filter_pos=[1, 3, 5]))

>>> [D(1), minor-second(1), F(3), major-second(2), A(5)]
```