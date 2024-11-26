import React, { useContext, useEffect } from 'react';
import { DemoContext } from '../../../../../context/DemoContext';
import { FilePicker as NeFilePicker } from '@nintexglobal/earthling-react';

const FileInput = ({ fieldData }) => {
    const { setInputValues, submitClicked, inputValues } = useContext(DemoContext);
    const title = fieldData.title.replace(/\s/g, '');

    useEffect(() => {
        if (fieldData.value && fieldData.value !== '' && !inputValues[title]) {
            setInputValues((prevValues) => ({ ...prevValues, [title]: fieldData.value }));
        }
    }, [fieldData.value, inputValues, setInputValues, title]);

    const handleFileChange = (pickedFiles, title) => {
        const formattedTitle = title.replace(/\s/g, '');
        if (!pickedFiles.length) {
            setInputValues((prevValues) => ({ ...prevValues, [formattedTitle]: [] }));
            return;
        }

        const encodedFiles = [];
        const readerPromises = [];

        for (let i = 0; i < pickedFiles.length; i++) {
            const reader = new FileReader();
            const file = pickedFiles[i];

            readerPromises.push(
                new Promise((resolve, reject) => {
                    reader.onload = () => {
                        const encoded = btoa(reader.result);
                        encodedFiles[i] = encoded;
                        resolve();
                    };
                    reader.onerror = () => {
                        console.log(reader.error);
                        reject();
                    };
                    reader.readAsBinaryString(file);
                })
            );
        }

        Promise.all(readerPromises)
            .then(() => {
                const value = encodedFiles.length === 1 ? encodedFiles[0] : encodedFiles;
                setInputValues((prevValues) => ({ ...prevValues, [formattedTitle]: value }));
            })
            .catch(() => {
                setInputValues((prevValues) => ({ ...prevValues, [formattedTitle]: [] }));
            });
    };

    return (
        <NeFilePicker
            className="inputField"
            onChange={(files) => handleFileChange(files, title)}
            singleFile={fieldData.single}
            accepts={fieldData.accepts ? fieldData.accepts : null}
            validationState={(fieldData.required && submitClicked && !inputValues[title]) ? 'error' : 'default'}
            validationMessage='This field is required.'
        />
    )
}

export default FileInput