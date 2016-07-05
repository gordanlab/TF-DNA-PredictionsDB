// Dna sequence(ATGC) with appropriate color for each letter.
// Example: <ColorDNA seq="ATGC" />
import React from 'react';

const CHAR_TO_COLOR = {
    'A': '#00CC00',
    'C': '#0000CC',
    'G': '#CCCC1A',
    'T': '#CC001A',


};
const FONT_FAMILY = 'monospace';
const FONT_SIZE = '12pt';

class ColorDNA extends React.Component {
    determineColor(c) {
        var color = CHAR_TO_COLOR[c];
        if (!color) {
            color = 'black'
        }
        return color;
    }

    coloredLetterSpan(key, c) {
        var color = this.determineColor(c);
        var style = {
            'color': color,
            'font-family': FONT_FAMILY,
            'font-size': FONT_SIZE,
        };
        return <span key={key} style={style}>{c}</span>;
    }

    render() {
        var seq = this.props.seq;
        var letters = [];
        for (var i = 0; i < seq.length; i++) {
            var c = seq[i];
            var key = i + "_" + c;
            letters.push(this.coloredLetterSpan(key, c));
        }
        return <div>
            {letters}
        </div>;
    }
}

export default ColorDNA;