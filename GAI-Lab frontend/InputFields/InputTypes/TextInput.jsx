import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import { TextField } from '@mui/material';

const TextInput = ({ fieldData }) => {
    const { inputValues, setInputValues, submitClicked } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    const handleTextChange = (event, title) => {
        setInputValues((prevValues) => ({ ...prevValues, [title]: event.target.value }));
    };

    useEffect(() => {
        if (fieldData.value && fieldData.value !== '' && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.value }));
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    return (
        <TextField
            type={fieldData.type === 'Number' ? 'number' : 'text'}
            size={fieldData.type !== 'Text-Long' ? 'small' : 'normal'} 
            multiline={fieldData.type === 'Text-Long'}
            rows={fieldData.type === 'Text-Long' ? 2 : 1}
            
            fullWidth
            className="inputField" 
            placeholder={fieldData.placeholder}
            value={inputValues[title] || ''}
            onChange={(event) => handleTextChange(event, title)}

            error={fieldData.required && submitClicked && !inputValues[title]}
            helperText={(fieldData.required && submitClicked && !inputValues[title]) ? 'This field is required' : ''}
        />
    )
}

export default TextInput;
