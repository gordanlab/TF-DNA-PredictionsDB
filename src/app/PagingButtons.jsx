import React from 'react';

class PagingButtons extends React.Component {
    constructor(props) {
        super(props);
    }

    onClickPage(page, evt) {
        evt.preventDefault();
        if (page > 0) {
            this.props.change_page(page);
        }
    }

    make_number_button(page_num, selected) {
        var props = {};
        var child = '';
        if (selected) {
            props['className'] = 'active';
            child = <span className="sr-only">(current)</span>;
        }
        var func = this.onClickPage.bind(this, page_num);
        return <li {...props} ><a href="#" style={{width: '3em', textAlign: 'center'}} onClick={func}>{page_num} {child}</a></li>;
    }

    make_labeled_button(label, disabled, page_num) {
        var props = {};
        if (disabled) {
            props['className'] = 'disabled';
        }
        var func = this.onClickPage.bind(this, page_num);
        return <li {...props} ><a href="#" onClick={func}><span>{label}</span></a></li>;
    }

    make_buttons(start_page, current_page, end_page) {
        var disable_prev = current_page === 1;
        var disable_next = false;
        var buttons = [];
        buttons.push(this.make_labeled_button('<', disable_prev, current_page - 1));
        for (var i = start_page; i <= end_page; i++) {
            buttons.push(this.make_number_button(i, i === current_page))
        }
        buttons.push(this.make_labeled_button('>', disable_next, current_page + 1));
        return buttons;
    }

    render() {
        var buttons = this.make_buttons(
            parseInt(this.props.start_page),
            parseInt(this.props.current_page),
            parseInt(this.props.end_page));

        return <ul className="pagination">
            {buttons}
        </ul>

    }
}

export default PagingButtons;