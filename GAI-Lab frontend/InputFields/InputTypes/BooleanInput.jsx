import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import { Switch } from '@mui/material';

const BooleanInput = ({ fieldData }) => {
    const { inputValues, setInputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    const handleBooleanChange = (event, title) => {
        setInputValues((prevValues) => ({ ...prevValues, [title]: event.target.checked }));
    };

    useEffect(() => {
        if (!inputValues.hasOwnProperty(title)) {
            if (fieldData.value) {
                setInputValues(prevValues => ({ ...prevValues, [title]: fieldData.value }));
            } else {
                setInputValues((prevValues) => ({ ...prevValues, [title]: false }));
            }
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    return (
        <Switch
            className="inputField"
            checked={inputValues[title]}
            onChange={(event) => handleBooleanChange(event, title)}
        />
    )
}

export default BooleanInput