import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import { DateTimePicker, DatePicker } from '@mui/x-date-pickers';

const DateTimeInput = ({ fieldData }) => {
    const { inputValues, setInputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    const handleDateChange = (date, title) => {
        setInputValues((prevValues) => ({ ...prevValues, [title]: date }));
    };

    useEffect(() => {
        if (fieldData.value && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.value }));
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    return (
        <DateTimePicker
            className="inputField"
            value={inputValues[title] || null}
            onChange={(date) => handleDateChange(date, title)}
        />
    )
}

const DateInput = ({ fieldData }) => {
    const { inputValues, setInputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    const handleDateChange = (date, title) => {
        setInputValues((prevValues) => ({ ...prevValues, [title]: date }));
    };

    useEffect(() => {
        if (fieldData.value && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.value }));
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    return (
        <DatePicker
            className="inputField"
            value={inputValues[title] || null}
            onChange={(date) => handleDateChange(date, title)}
        />
    );
};

export { DateTimeInput, DateInput };
