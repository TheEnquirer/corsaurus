import './search.css';
import React, { Component } from 'react';
import autoBind from 'react-autobind';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

class Search extends Component 
{
    constructor(props) 
    {
        super(props);
        autoBind(this);

        this.state = { 
            mounted: false, 
            firstTime: true,
            data: [],
            errormsg: "",
            inputval: "",
            prevSearch: "",
        };
    }

    clearOnFirstEnter(e) {
        if (this.state.firstTime) {
            //e.target.innerHTML = "&nbsp;";
            e.target.innerHTML = "";
            this.setState({ firstTime: false });
        }
    }
    getCaretPosition (node) {
        // from https://stackoverflow.com/a/46902361/10372825
        var range = window.getSelection().getRangeAt(0),
            preCaretRange = range.cloneRange(),
            caretPosition,
            tmp = document.createElement("div");

        preCaretRange.selectNodeContents(node);
        preCaretRange.setEnd(range.endContainer, range.endOffset);
        tmp.appendChild(preCaretRange.cloneContents());
        caretPosition = new DOMParser().parseFromString(tmp.innerHTML, 'text/html');
        return caretPosition.body.textContent.length;
    }
    setCaretPosition(pos, element) {
        // based on https://stackoverflow.com/a/24862437/10372825
        // only works for one layer of nested nodes
        function get_text_nodes_in(node) {
            var text_nodes = [];
            if (node.nodeType === 3) {
                text_nodes.push(node);
            } else {
                var children = node.childNodes;
                for (var i = 0, len = children.length; i < len; ++i) {
                    text_nodes.push.apply(text_nodes, get_text_nodes_in(children[i]));
                }
            }
            return text_nodes;
        }
        var range = document.createRange();
        range.selectNodeContents(element);
        var text_nodes = get_text_nodes_in(element);
        let foundStart = false;
        let char_count = 0, end_char_count = 0;

        // loop through text nodes until we find the one that contains the target
        for (let cur of text_nodes) {
            end_char_count = char_count + cur.length;
            if (pos >= char_count && pos < end_char_count) {
                range.setStart(cur, pos - char_count);
                range.setEnd(cur, pos - char_count);
                foundStart = true;
                break;
            }
            char_count = end_char_count;
        }
        if (!foundStart) {
            const last_node = text_nodes[text_nodes.length-1];
            if (typeof last_node == 'undefined') return;
            //range.setEnd(last_node, last_node.length);
            range.selectNodeContents(element);
            range.collapse(false);
        }

        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }

    parseString(v, innerHTMLSetter=null, target=null) 
    {
        let pos = [];
        let neg = [];
        let lp = 0;
        let p = "+";
        let full = [];
        let mods = [];
        let tok_info = [];

        this.pusher = (i) => {
            let mod = v.slice(lp, i).replace(/((?<!\\)[+-\\])+/, "").trim();
            // eslint-disable-next-line
            if (p == '+') { pos.push(mod) } else { neg.push(mod) }
            full.push(mod); // NOTE: could get rid of this and combine error parsing below with the other `let bad = false`
            mods.push(mod);

            let bad = false;
            if (mod.length === 0) bad = true;

            tok_info.push([bad ? 'err' : (p === '+' ? 'pos' : 'neg'), lp, i]);
        }

        for (let i in v) 
        {
            // eslint-disable-next-line
            if ((v[i-1] != "\\") && ((v[i] == '-') || (v[i] == '+'))) 
            {
                // eslint-disable-next-line
                if (i != lp) // NOTE: exr0n doesn't understand why we need this if statement
                {
                    this.pusher(i);
                    lp = i;
                }
                p = v[i];
            }
            // eslint-disable-next-line
            if (i == v.length - 1) { this.pusher(i+1) } 
        }

        if (full.length === 0) { return [0, ""] }
        let bad = false; 
        //console.log(full); // for debugging space inclusion
        for (let i in full) {
            const [ color, lhs, rhs ] = tok_info[i];
            //console.log(full[i]); // for debugging space inclusion
            if (full[i].includes(" ") || full[i].includes(String.fromCharCode(160))) { 
                bad = true;
                full[i] = `<span class="syntaxhlerr">${v.slice(lhs, rhs)}</span>`;
            } else {
                full[i] = `<span class="syntaxhl${color}">${v.slice(lhs, rhs)}</span>`;
            }
        }
        if (typeof innerHTMLSetter === 'function') innerHTMLSetter(full.join(""));

        if (bad) return [0, "Please seperate words with either + or -"];
        if (mods.filter(v => v.length === 0).length) return [0, "Extraneous operator"]; // NOTE: this logic handled both here and in pusher

        // out of vocab hl
        if (typeof innerHTMLSetter === 'function') 
            this.query({ 'mode': 'vocabcheck', 'words': mods })
                .then((wear_a_mask) => {
                    // Array.from() on nodeList: https://stackoverflow.com/a/32767009
                    const socially_distance = Array.from(target.childNodes).filter((v, i) => !wear_a_mask[i] && v.className !== 'syntaxhlerr');
                    if (socially_distance.length > 0) {
                        this.setState({ errormsg: `Unrecognized word${socially_distance.length > 1 ? 's' : ''} ${
                            JSON.stringify(mods.filter((_, i) => !wear_a_mask[i])).slice(1, -1).replace(/,/g, ", ")}` });
                        socially_distance.forEach(v => { v.className = 'syntaxhlerr'; });
                    }
                    //const wash_ur_hands = full.map((v, i) => wear_a_mask[i] ? v : v.replace(/syntaxhl(pos|neg)/, 'syntaxhlerr'));
                    //innerHTMLSetter(wash_ur_hands.join(""));
                }).catch(console.error);

        this.setState({ errormsg: '' });
        return [1, [pos, neg]];
    }

    cleanseInputNewlines(e) {
        // https://stackoverflow.com/a/33239883/10372825
        if (e.keyCode === 13) {
            this.handleSubmit(e);
            e.preventDefault();
        }
    }

    handleTextChange(e) {
        setTimeout(() => {
            let pos = this.getCaretPosition(e.target);
            if (e.target.innerHTML.length === 1) {
                e.target.innerHTML = '<span class="syntaxhlpos">' + e.target.innerHTML + '</span>';
            }
            // clense content of html
            // https://stackoverflow.com/a/47140708/10372825
            let val = new DOMParser().parseFromString(e.target.innerHTML, 'text/html');
            val = (val.body.textContent || "").replace(/&nbsp;/g, ' ').replace(/\n/g, ' ');
        
            this.setState({inputval: val.toLowerCase()});
            let [ ok, g ] = this.parseString(this.state.inputval, (v) => {
                e.target.innerHTML = v.replace(/ /g, '&nbsp;').replace(/<span&nbsp;class="syntaxhl(pos|neg|err)">/g, '<span class="syntaxhl$1">');
                this.setCaretPosition(pos, e.target); // set cursor to one after the previous position (bc setting innerHTML pushes cursor to front)
                //if (e.target.innerHTML.length == 0)
                //    e.target.innerHTML = '&nbsp;';
            }, e.target);
            if (!ok) this.setState({ 'errormsg': g }); // but then we clear the error with in the parse itself.... this should probably go in the parseString too
        }, 0);
    }

    handleSubmit() {
        if (this.state.inputval !== this.state.prevSearch) {
            this.setState({prevSearch: this.state.inputval});
            let parsed = this.parseString(this.state.inputval);
            if (parsed[0] === 1) {
                this.queryNearestWordvecs( 
                    {
                        'num': 100,
                        'pos': parsed[1][0],
                        'neg': parsed[1][1],
                        'mode': 'sum'
                    }
                );
            } else {
                this.setState({errormsg: parsed[1]});
            }
        }
    }

    queryNearestWordvecs(request)
    {
        this.query(request)
            .then(data => {
                this.setState({errormsg: ""})
                this.props.set(data)
                this.props.setShown(1)
            });
    }

    async query(req) {
        return fetch('/query', { method: 'put', body: JSON.stringify(req) })
            .then(res => res.json())
            .then(data => {
                if (data.hasOwnProperty('error'))
                    throw data.error;
                else
                    return data.success;
            })
            .catch(console.error);
    }

    componentDidMount() {
        this.setState({mounted: true})
        this.queryNearestWordvecs(
            {
                'num': 100,
                'pos': ['king', 'woman'],
                'neg': ['man'],
                'mode': 'sum'
            }
        )
    }

    render() {
        return (
            <div className="search-wrapper">
            <FontAwesomeIcon icon={faSearch} onClick={this.handleSubmit} className="icon"/>
            <div className="search-input" 
            onFocus={this.clearOnFirstEnter}
            onInput={this.handleTextChange}
            contentEditable={true}
            onKeyDown={this.cleanseInputNewlines}
            onPaste={this.clenseInputPaste}
            suppressContentEditableWarning={true /* iff you know what ur doing, which I don't https://stackoverflow.com/a/49639256/10372825 */}
            ><span className={"syntaxhlpos"}>king</span> <span className={"syntaxhlneg"}>- man</span> + <span className={"syntaxhlpos"}>woman</span></div>
            {(this.state.errormsg !== "")?
                <div className="errormsg"> 
                <FontAwesomeIcon icon={faExclamationTriangle} className="error-icon"/>
                {this.state.errormsg}
                </div>
                : ""}
            </div>
        )
    }
}

export default Search;
