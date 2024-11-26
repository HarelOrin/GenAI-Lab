import React from 'react'
import RenderSection from './RenderSection';
import RenderInput from './RenderInput';

const RenderField = ({ data }) => {
    return Object.entries(data).map(([fieldKey, fieldValue]) => (
        fieldValue.type === 'object'
        ? (<RenderSection key={fieldKey} data={fieldValue} />)
        : (
            <div className="inputContainer" key={fieldKey}>
                <div className="inputProperties">
                    {fieldValue.title && <span className="inputTitle">{fieldValue.title}</span>}
                    
                    {fieldValue.required &&  (
                        <b className="required" title='Required Field'>*</b>
                    )}
                    
                    {fieldValue.description && <div className="inputDescription">
                        {fieldValue.description}
                    </div>}
                </div>
                <RenderInput fieldData={fieldValue} />
            </div>
        )
    ));
}

export default RenderField