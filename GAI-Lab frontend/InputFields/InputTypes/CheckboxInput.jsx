import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import { FormControlLabel, Checkbox, FormControl } from '@mui/material';

const CheckboxInput = ({ fieldData }) => {
    const { inputValues, setInputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    useEffect(() => {
        if (!inputValues[title]) {
            if (fieldData.value && fieldData.value !== '') {
                setInputValues(prevValues => ({ ...prevValues, [title]: fieldData.value }));
            } else {
                const newInputValues = { ...inputValues, [title]: {} };
                fieldData.choices.forEach(choice => {
                    newInputValues[title][choice] = false;
                });
                setInputValues(newInputValues);
            }
        }
    }, [inputValues, setInputValues, title, fieldData.choices, fieldData.value]);

    const handleCheckboxChange = (event, title, choice) => {
        setInputValues((prevValues => ({ ...prevValues, [title]: { ...prevValues[title], [choice]: event.target.checked } })));
    };

    return (
        <FormControl className="inputField">
            {fieldData.choices.map((choice, index) => (
                <FormControlLabel key={index}
                    control={
                        <Checkbox checked={inputValues[title] ? inputValues[title][choice] : false} onChange={(event) => handleCheckboxChange(event, title, choice)} name={choice} />
                    }
                    label={choice}
                />
            ))}
        </FormControl>
    )
}

export default CheckboxInput