import React, { useEffect, useContext, useState } from 'react';
import { DemoContext } from '../../../../context/DemoContext';
import { getEndpointResponse, getSubendpointResponse } from '../../../../services/dataBaseEndpoints';
import { v4 as uuidv4 } from 'uuid';
import classnames from 'classnames';

import { Button as NeButton, ButtonSet as NeButtonSet } from '@nintexglobal/earthling-react';
import './InputFields.css';

import RenderSection from './Renders/RenderSection';

const InputFields = ({ projectId, endpoint }) => {
    const { setOutput, setIsWaiting, inputValues, setInputValues, isWaiting, setSubmitClicked } = useContext(DemoContext);
    const [inputForm, setInputForm] = useState(endpoint.inputSchema);
    
    useEffect(() => {
        setInputForm(endpoint.inputSchema);
    }, [endpoint]);

    const handleSubmit = async (funcName) => {
        setSubmitClicked(true);
        setIsWaiting(true);
        console.log('inputValues:', inputValues);
        const requestId = uuidv4();
        const args = btoa(encodeURIComponent(JSON.stringify(inputValues)));
        
        const variables = `args: "${args}", requestId: "${requestId}"`
        const formattedFuncName = funcName.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());

        const response = await getEndpointResponse(projectId, inputForm.schemaType, formattedFuncName, variables);
        
        setOutput({ ...response, requestId })

        setIsWaiting(false);
    };

    const handleManipulate = async (funcName) => {
        setIsWaiting(true);

        const requestId = uuidv4();
        const args = btoa(JSON.stringify(inputValues));

        const variables = `args: "${args}", requestId: "${requestId}"`;
        const formattedFuncName = funcName.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());

        const response = await getSubendpointResponse(projectId, inputForm.schemaType, formattedFuncName, variables);       

        setInputValues({});
        setInputForm(response);
        setIsWaiting(false);
    };

    return (
        <div className='inputFieldsContainer'>
            <div className="sectionContainer description">
                <div className="sectionTitle firstTitle"> Demo Description </div>
                <div className='sectionContent first'>
                    {endpoint.demoDescription}
                </div>
            </div>
            <div className="dynamicInput">
                <RenderSection data={inputForm.input} />
            </div>
            <NeButtonSet showTopDivider>
            {inputForm.buttons.map((button, index) => {
                if (button.type === 'output') {
                    return (
                        <NeButton
                            key={index}
                            onClick={() => handleSubmit(button.funcName)}
                            showSpinner={isWaiting}
                            className="submitButton"
                            variant='primary'
                        >
                            Submit
                        </NeButton>
                    );
                } else if (button.type === 'manipulation') {
                    return (
                        <NeButton
                            key={index}
                            onClick={() => handleManipulate(button.funcName)}
                            showSpinner={isWaiting}
                            className="manipulationButton"
                            variant={
                                index === 0 ? 'primary' : 'secondary'
                            }
                        >
                            {button.name}
                        </NeButton>
                    );
                } else {
                    return null;
                }
            })}
            </NeButtonSet>
            <div className={classnames(
                'waiting', { 'hide': !isWaiting }
            )}>
                Loading response, This may take a while...
            </div>
        </div>
    );
};

export default InputFields;
