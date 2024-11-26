 
import React, { useContext, useState, useEffect } from 'react'
import { IconButton, Select, TextField, MenuItem } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import Button from '@mui/material/Button';
import { DemoContext } from '../../../../../context/DemoContext';

const SkuidFieldsForm = (SkuidFieldsForm) => {

    const { inputValues, setInputValues } = useContext(DemoContext);
    const [newEntry, setNewEntry] = useState({});
    const [pervSkuidFieldsForm, setPervSkuidFieldsForm] = useState({});

    useEffect(() => { 
        if (SkuidFieldsForm && JSON.stringify(SkuidFieldsForm) != JSON.stringify({}) && !inputValues["SkuidFieldsForm"] && JSON.stringify(SkuidFieldsForm) !== JSON.stringify(pervSkuidFieldsForm)) {            
            const temp = atob(SkuidFieldsForm.src);
            const parsedData = JSON.parse(temp)
            setInputValues((prevState) => ({...prevState, ["SkuidFieldsForm"]: {'fields': parsedData.fields, 'properties': parsedData.properties}})); 
            setPervSkuidFieldsForm(SkuidFieldsForm)         
        }
    }, [SkuidFieldsForm, inputValues, setInputValues]);
    
    const handleFieldChange = (index, key, value) => {
        const updatedFields = [...inputValues.SkuidFieldsForm.fields];
        updatedFields[index][key] = value;
        updateData('fields', updatedFields)   
    };
    
    const handlePropertiesChange = (key, value) => {
        const updatedProperties = {...inputValues.SkuidFieldsForm.properties}
        updatedProperties[`${key}`] = value
        updateData('properties', updatedProperties)
    }

    const removeField = (index) => {
        const updatedFields = [...inputValues.SkuidFieldsForm.fields];
        updatedFields.splice(index, 1);
        updateData('fields', updatedFields)
    }

    const removeEntry = (e, fieldIndex, entryIndex) => {
        e.preventDefault(); 
        const updatedFields = [...inputValues.SkuidFieldsForm.fields];
        updatedFields[fieldIndex].entries.splice(entryIndex, 1)
        updateData('fields', updatedFields)
        
    }

    const newField = (e) => {
        e.preventDefault(); 
        const updatedFields = [...inputValues.SkuidFieldsForm.fields];
        updatedFields.push({"fieldName": '', "fieldType": "TEXT"});
        updateData('fields', updatedFields)
    }

    const handleEntriesSubmit = (e, index) => {
        e.preventDefault();
        const updatedFields = [...inputValues.SkuidFieldsForm.fields];
        if (!updatedFields[index]['entries']) {
            updatedFields[index]['entries'] =[]
        }
        if (newEntry[index]) {
            updatedFields[index]['entries'].push(newEntry[index]);
            updateData('fields', updatedFields)
            setNewEntry(prevState => ({
                ...prevState,
                [index]: ''
            }));
        }
    }

    const handleEntriesChange = (index, value) => {
        setNewEntry(prevState => ({
            ...prevState,
            [index]: value 
        }));
    };   


    const updateData = (title, value) => {
        setInputValues(prevData => ({
            ...prevData, 
            ['SkuidFieldsForm']: {...prevData['SkuidFieldsForm'], [title]: value}
        }));
    };
    
    return (
        <div>
            {inputValues.SkuidFieldsForm && inputValues.SkuidFieldsForm.fields && inputValues.SkuidFieldsForm.properties.appName && 
            <form>
                <div>
                    {inputValues.SkuidFieldsForm.fields.map((field, index) => (
                        <div key={index} style={{ marginBottom: '10px' }}>
                            <label>
                            <strong> Field Name: &nbsp;</strong>
                                <TextField
                                    className="inputField" 
                                    size='small'
                                    type="text"
                                    value={field.fieldName}
                                    onChange={(e) => handleFieldChange(index, 'fieldName', e.target.value)}
                                    />
                            </label>
                            <label>
                                <strong> &nbsp; Field Type: &nbsp; </strong>
                                <Select
                                    size="small"
                                    value={field.fieldType}
                                    onChange={(e) => handleFieldChange(index, 'fieldType', e.target.value)}
                                    >
                                    <MenuItem value="TEXT">TEXT</MenuItem>
                                    <MenuItem value="NUMBER">NUMBER</MenuItem>
                                    <MenuItem value="PERCENT">PERCENT</MenuItem>
                                    <MenuItem value="DATE">DATE</MenuItem>
                                    <MenuItem value="DATETIME">DATETIME</MenuItem>
                                    <MenuItem value="EMAIL">EMAIL</MenuItem>
                                    <MenuItem value="PICKLIST">PICKLIST</MenuItem>
                                </Select>
                                <Button size="small" variant="contained" type="button" style={{ marginLeft: '10px' }} onClick={() => removeField(index)}>Remove field</Button>
                                {field.fieldType === 'PICKLIST' && (
                                    <div style={{ marginTop: '10px', marginLeft: '20px' }}>
                                        <label style={{ marginBottom: '5px' }} >
                                        <strong >Picklist Entries: &nbsp;</strong>
                                            <div style={{ display: 'flex', alignItems: 'center' }} >
                                            {field.entries?.map((entry, i) => (
                                                <div style={{ display: 'flex', marginBottom: "5px"}}>
                                                    <strong>{entry}</strong>
                                                        <IconButton aria-label="delete" onClick={(e) => removeEntry(e, index, i)} size="small">
                                                            <DeleteIcon fontSize="inherit" style={{ marginRight: '12px', marginLeft: '-3px' }} />
                                                        </IconButton>
                                                </div>
                                            ))}
                                            <TextField
                                                type="text"
                                                size='small'
                                                value={newEntry[index] || ''}
                                                onChange={(e) => handleEntriesChange(index, e.target.value)}
                                                />
                                            <Button size="small"  variant="contained" type="button" style={{ marginLeft: '5px' }} onClick={(e) => handleEntriesSubmit(e, index)}>Add entry</Button>
                                            </div>
                                        </label>
                                    </div>
                                )}
                            </label>
                        </div>
                    ))}
                    <Button size="small" variant="contained" type="button" style={{ marginBottom: '10px' }} onClick={newField}>Add field</Button>
                </div>
                {inputValues.SkuidFieldsForm.properties && inputValues.SkuidFieldsForm.properties.appName && <>
                <div style={{ marginBottom: '10px' }}>
                    <div style={{ marginBottom: '10px', marginTop: '10px' }} >App Properties:</div>
                    <label style={{ display: 'flex', alignItems: 'center'}}>
                    <strong>App Name: &nbsp; </strong>
                        <TextField
                            size='small'
                            type='text'
                            value={inputValues.SkuidFieldsForm.properties.appName || ''}
                            onChange={(e) => handlePropertiesChange('appName', e.target.value)}
                            />
                    </label>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label style={{ display: 'flex', alignItems: 'center'}}>
                    <strong>Page Name: &nbsp;</strong> 
                        <TextField
                            size='small'
                            type='text'
                            value={inputValues.SkuidFieldsForm.properties.pageName || ''}
                            onChange={(e) => handlePropertiesChange('pageName', e.target.value)}
                            />
                    </label>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label style={{ display: 'flex', alignItems: 'center'}}>
                    <strong>Database Name: &nbsp;</strong>
                        <TextField
                            size='small'
                            type='text'
                            value={inputValues.SkuidFieldsForm.properties.databaseName || ''}
                            onChange={(e) => handlePropertiesChange('databaseName', e.target.value)}
                            />
                    </label>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label style={{ display: 'flex', alignItems: 'center'}}>
                    <strong>Object Name: &nbsp;</strong>
                        <TextField
                            size='small'
                            type='text'
                            value={inputValues.SkuidFieldsForm.properties.objectName || ''}
                            onChange={(e) => handlePropertiesChange('objectName', e.target.value)}
                            />
                    </label>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label style={{ display: 'flex', alignItems: 'center'}}>
                    <strong>Model Name: &nbsp;</strong>
                        <TextField
                            size='small'
                            type='text'
                            value={inputValues.SkuidFieldsForm.properties.modelName || ''}
                            onChange={(e) => handlePropertiesChange('modelName', e.target.value)}
                            />
                    </label>
                </div>
                <div style={{ marginBottom: '10px' }}>
                    <label style={{ display: 'flex', alignItems: 'center'}}>
                    <strong>Case: &nbsp;</strong>
                        <TextField
                            size='small'
                            type='text'
                            value={inputValues.SkuidFieldsForm.properties.case || inputValues.properties.appName}
                            onChange={(e) => handlePropertiesChange('case', e.target.value)}
                            />
                    </label>
                </div>
            </>}
            </form>}
        </div>
    )
}
 
export default SkuidFieldsForm