import { Summary } from "../types";
import testSummaries from "../test/test_summaries.json";
import { useEffect, useState } from "react";
import styled from "styled-components";

type SearchResultsProps = {
    selectedCategories: any[];
};

const SearchResults = (props: SearchResultsProps) => {
    const [results, updateResults] = useState([] as Summary[]);

    useEffect(() => {
        // fetch search results based on props.selectedCategories
        // TODO

        updateResults(testSummaries);
    }, []);

    return (
        <div style={{}}>
            {results.map(r => (
                <Result href={r.url}>
                    <Img src={r.thumbnail} />
                    <Description>{r.description}</Description>
                </Result>
            ))}
        </div>
    );
};

export default SearchResults;

const Result = styled.a`
    display: flex;
    text-decoration: none;
    color: black;
    align-items: center;
    padding: 10px;
    background-color: #e1e1e1;
    border-radius: 10px;
    margin: 20px 0;
    &:hover {
        cursor: pointer;
        background-color: #fff1ac;
    }
`;

const Img = styled.img`
    border-radius: 10px;
    width: 15%;
`;

const Description = styled.div`
    text-align: center;
    width: 85%;
    font-size: 25px;
`;
