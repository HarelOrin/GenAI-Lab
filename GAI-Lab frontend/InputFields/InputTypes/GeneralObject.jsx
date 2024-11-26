import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';

const GeneralObject = ({ fieldData }) => {
    const { inputValues, setInputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    useEffect(() => {
        if (!inputValues.hasOwnProperty(title)) {
            if (fieldData.value) {
                setInputValues(prevValues => ({ ...prevValues, [title]: fieldData.value }));
            }
        }
    }, [inputValues, setInputValues, title]);

    return (
        <div className='invisObject'/>
    )
}

export default GeneralObject