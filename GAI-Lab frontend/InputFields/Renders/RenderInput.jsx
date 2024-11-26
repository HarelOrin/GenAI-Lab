import React from 'react'
import * as InputTypes from '../InputTypes';

const RenderInput = ({ fieldData }) => {
    switch (fieldData.type) {
        case 'Number': case 'Text-Long': case 'Text-Short':
            return <InputTypes.TextInput fieldData={fieldData} />;
        case 'Boolean':
            return <InputTypes.BooleanInput fieldData={fieldData} />;
        case 'DateTime':
            return <InputTypes.DateTimeInput fieldData={fieldData} />;
        case 'Date':
            return <InputTypes.DateInput fieldData={fieldData} />;
        case 'File upload':
            return <InputTypes.FileInput fieldData={fieldData} />;
        case 'Choice-Single':
            return <InputTypes.SelectInput fieldData={fieldData} />;
        case 'Choice-Multiple':
            return <InputTypes.CheckboxInput fieldData={fieldData} />;
        case 'Form-Display':
            return <InputTypes.FormDisplay fieldData={fieldData} />;
        case 'chat-history':
            return <InputTypes.ChatHistory fieldData={fieldData} />;
        case 'Link':
            return <a href={fieldData.url} target="_blank" rel="noreferrer" className="inputField">{fieldData.urlDisplay}</a>;
        case 'Image':
            return <img src={fieldData.src} alt={fieldData.title} className="inputField" />;
        case 'Text-Display':
            return ''
        case 'iFrame':
            return <iframe src={fieldData.src} width={fieldData.width} height={fieldData.height}title={fieldData.title}></iframe>
        case 'General-Object':
            return <InputTypes.GeneralObject fieldData={fieldData} />;
        case 'Render-Json':
            return <InputTypes.RenderJson src={fieldData.data} />
        case 'Skuid-Form':
            return <InputTypes.SkuidFieldsForm src={fieldData.data} />
        
        default:
            return null;
    }
}

export default RenderInput