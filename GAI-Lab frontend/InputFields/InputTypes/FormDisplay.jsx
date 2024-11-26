import React, {useContext, useEffect} from 'react';
import { DemoContext } from '../../../../../context/DemoContext';

import { renderForm } from '../../Output/FormGenerator/FormGenerator';
import '../../Output/FormGenerator/FormGenerator.css';

const FormDisplay = ({ fieldData }) => {
    const { setInputValues, inputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');
    
    useEffect(() => {
        if (fieldData.value && fieldData.value !== '' && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.value }));
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    return renderForm(fieldData.json, true);
};
  
  export default FormDisplay;