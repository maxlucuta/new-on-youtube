import { SetStateAction } from "react";
import { MultiValue, ActionMeta } from "react-select";
import Select from "react-select";
import styled from "styled-components";
import { MAX_TOPICS } from "../functions";
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

type SearchPageBarProps = {
    selection: string[];
    availableTopics: string[];
    updateSelection: (value: SetStateAction<string[]>) => void
}

type SelectOption = {
    label: string;
    value: string;
}

const CustomAlert = withReactContent(Swal);

const SearchPageBar = (props: SearchPageBarProps) => {


    const handleChange = (newValue: MultiValue<SelectOption>, actionMeta: ActionMeta<SelectOption>) => {
        if (newValue.length > MAX_TOPICS) CustomAlert.fire({
            icon: "error",
            title: <AlertMessage>Sorry, you can only search for {MAX_TOPICS} topics at a time</AlertMessage>,
            });
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
            placeholder = {<PlaceholderText>Select topics</PlaceholderText>}
            noOptionsMessage={() => 'That topic is not yet in our database. Please create a New On YouTube account to search for custom topics.'}
            styles={{
                control: (baseStyles, state) => ({
                ...baseStyles,
                borderColor: 'black',
                }),
                multiValue: (base) => ({
                    ...base,
                    padding: `5px`,
                    margin: `5px`,
                    fontSize: `16px`
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


const AlertMessage = styled.div`
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif
`;