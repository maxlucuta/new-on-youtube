import { Dispatch, SetStateAction, useEffect, useState } from "react";
import styled from "styled-components";
import testCategories from "../test/test_categories.json";

type CategorySelectorProps = {
    selectedCategories: string[];
    updateSelectedCategories: Dispatch<SetStateAction<any[]>>;
};

const CategorySelector = (props: CategorySelectorProps) => {
    const [categories, updateCategories] = useState([] as string[]);

    useEffect(() => {
        // fetch categories here with axios request
        // TODO

        updateCategories(testCategories);
    }, []);

    const updateSelection = (c: string) => {
        if (props.selectedCategories.includes(c))
            props.updateSelectedCategories(sc => {
                return sc.filter(cat => cat != c);
            });
        else
            props.updateSelectedCategories(sc => {
                return sc.concat([c]);
            });
    };

    return (
        <div
            style={{
                display: "flex",
                width: "500px",
                flexWrap: "wrap",
                margin: "auto",
                justifyContent: "center",
                marginTop: "20px",
            }}>
            {categories.map(c => (
                <CategoryButton
                    onClick={() => updateSelection(c)}
                    selected={props.selectedCategories.includes(c)}>
                    {c}
                </CategoryButton>
            ))}
        </div>
    );
};

export default CategorySelector;

const CategoryButton = styled.button<{ selected: boolean }>`
    margin: 10px;
    font-size: 30px;
    padding: 10px;
    border-style: none;
    background-color: ${props => (props.selected ? "#FAD000" : "grey")};
    border-radius: 5px;
    &:hover {
        transform: scale(1.1);
        cursor: pointer;
    }
`;
