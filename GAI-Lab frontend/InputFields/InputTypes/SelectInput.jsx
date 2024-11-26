import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import { Select, MenuItem, InputLabel, FormControl, FormHelperText } from '@mui/material';

const SelectInput = ({ fieldData }) => {
    const { inputValues, setInputValues, submitClicked } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    useEffect(() => {
        if (fieldData.value && fieldData.value !== '' && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.value }));
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    const handleSelectChange = (event, title) => {
        setInputValues((prevValues) => ({ ...prevValues, [title]: event.target.value }));
    };

    return (
        <FormControl fullWidth className="inputField">
            <InputLabel id={title}>{fieldData.title}</InputLabel>
            <Select
                labelId={title}
                label={fieldData.title}
                value={inputValues[title] || ''}
                onChange={(event) => handleSelectChange(event, title)}
            >
                {fieldData.choices.map((choice, index) => (
                    <MenuItem key={index} value={choice}>{choice}</MenuItem>
                ))}
            </Select>
            {(fieldData.required && submitClicked && !inputValues[title]) && <FormHelperText error>This field is required</FormHelperText>}
        </FormControl>
    )
}

export default SelectInput