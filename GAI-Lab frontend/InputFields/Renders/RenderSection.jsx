import React from 'react'
import RenderField from './RenderField';
import classNames from 'classnames'

const RenderSection = ({ data }) => {
    const invisible = data.objectType?.invisible ? true : false;
    const horizontal = data.objectType?.horizontal ? true : false;
    const first = data.objectType?.first ? true : false;
    
    return (
        <div className={classNames('sectionContainer', { 'invisSection': invisible })}>
            <div className={classNames('sectionTitle', { 'firstTitle': first })}>
                {data.title}
            </div>
            <div className={classNames(
                'sectionContent', { 
                'horizontal': horizontal,
                'first': first }
            )}>
                <RenderField data={data.properties} />
            </div>
        </div>
    )
}

export default RenderSection