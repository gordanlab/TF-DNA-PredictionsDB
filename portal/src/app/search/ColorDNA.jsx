// Dna sequence(ATGC) with appropriate color for each letter.
// Example: <ColorDNA seq="ATGC" />
import React from 'react';

const CHAR_TO_COLOR = {
    'A': '#00d000',
    'C': '#0729d3',
    'G': '#fdbc00',
    'T': '#d71f00',
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

    coloredLetterSpan(key, c, underscore) {
        var color = this.determineColor(c.toUpperCase());
        var style = {
            'color': color,
            'fontFamily': FONT_FAMILY,
            'fontSize': FONT_SIZE,
        };
        if (underscore) {
            style['borderBottom'] = '1px solid black';
        }
        return <span key={key} style={style}>{c}</span>;
    }

    render() {
        var {seq, coreOffset, coreLength} = this.props;
        var letters = [];
        for (var i = 0; i < seq.length; i++) {
            var c = seq[i];
            // reactjs requires a key for dynamic component lists
            var key = i + "_" + c;
            let underscore = false;
            if (coreOffset && coreLength) {
                underscore = i >= coreOffset && i < coreOffset + coreLength;
            }
            letters.push(this.coloredLetterSpan(key, c, underscore));
        }
        return <div>
            {letters}
        </div>;
    }
}

export default ColorDNA;