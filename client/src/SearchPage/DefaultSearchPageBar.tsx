import { SetStateAction } from "react";
import { MultiValue, ActionMeta } from "react-select";
import Select from "react-select";
import styled from "styled-components";
import { MAX_TOPICS } from "../functions";

type SearchPageBarProps = {
    selection: string[];
    availableTopics: string[];
    updateSelection: (value: SetStateAction<string[]>) => void
}

type SelectOption = {
    label: string;
    value: string;
}

const SearchPageBar = (props: SearchPageBarProps) => {


    const handleChange = (newValue: MultiValue<SelectOption>, actionMeta: ActionMeta<SelectOption>) => {
        if (props.selection.length > MAX_TOPICS) alert("Maximum of 20 topics allowed.");
        else props.updateSelection(newValue.map(nv => nv.value));
    }

    return (
        <Select
            value = {props.selection.map(t => { return {value: t, label: t} })}
            options = {props.availableTopics.map(t => { return {value: t, label: t} })}
            isClearable=  {true}
            isSearchable = {true}
            isMulti = {true}
            onChange = {handleChange}
            placeholder={<PlaceholderText>Select topics</PlaceholderText>}
            styles={{
                control: (baseStyles, state) => ({
                ...baseStyles,
                borderColor: 'black',
                }),
            
            }}
            theme={(theme) => ({
                ...theme,
                borderRadius: 0,
                colors: {
                    ...theme.colors,
                    primary25: 'var(--colour-background-grey)',
                    primary: 'none',
                },
            })}
        />
    )
}

export default SearchPageBar


const PlaceholderText = styled.div`
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
`;