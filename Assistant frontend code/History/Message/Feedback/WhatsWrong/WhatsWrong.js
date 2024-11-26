import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';

import PropTypes from 'prop-types';
import classNames from 'classnames';

import { sendFeedback } from '../../../../../../contexts';

import './WhatsWrong.css';

import { ToggleButton, ToggleButtonGroup, IconButton, TextField } from '@mui/material';
import { Button as NeButton } from '@nintexglobal/earthling-react';
import CloseIcon from '@mui/icons-material/Close';


const WhatsWrong = ({ showFeedback, messageId, handleFeedbackClick }) => {
	// Local state to manage checkbox values and description
	const { t } = useTranslation();
	const [checkboxValues, setCheckboxValues] = useState([]);
	const [description, setDescription] = useState('');
	const [email, setEmail] = useState('');
	const [isFormEmpty, setIsFormEmpty] = useState(true);

	// Handle checkbox changes
	const handleCheckboxChange = (event, value) => {
		setIsFormEmpty(false);
		setCheckboxValues(value);
	};

	const handleDescrptionChange = (event) => {
		setIsFormEmpty(false);
		setDescription(event.target.value);
	};

	const handleEmailChange = (event) => {
		setIsFormEmpty(false);
		setEmail(event.target.value);
	};

	// Handle sending feedback
	const handleSendClick = () => {
		const descriptionText = description.trim() !== '' ? description : null;
		const checkboxString = checkboxValues.length > 0 ? checkboxValues.join('. ') : null;
		const fullDescription = `${checkboxString}. ${descriptionText}`;
		const emailToSend = email.trim() !== '' ? email : null;

		sendFeedback(messageId, 'dislike', fullDescription, emailToSend);
		handleFeedbackClick(event, 'done');
	};

	return (
		<div className={classNames(
			'whats-wrong-wrapper',
			{'hidden': !showFeedback}
		)}>

			<div className='whats-wrong-header'>
				<b>{t('feedback.sentences.whyNotSatisfying')}</b>
				<IconButton style={{ marginLeft: 'auto' }} onClick={() => handleFeedbackClick(event, 'done')} >
					<CloseIcon />
				</IconButton>
			</div>

			<ToggleButtonGroup
				className='button-group'
				size="small"
				value={checkboxValues}
				onChange={handleCheckboxChange} 
			>
				<ToggleButton
					value="Incomplete" aria-label='Incomplete'
					className={classNames(
						'checkbox-button',
						{'selected': checkboxValues.includes('Incomplete')}
					)}>
					{t('feedback.checkboxes.incomplete')}
				</ToggleButton>
				<ToggleButton
					value="Inaccurate" aria-label='Inaccurate'
					className={classNames(
						'checkbox-button',
						{'selected': checkboxValues.includes('Inaccurate')}
					)}>
					{t('feedback.checkboxes.inaccurate')}
				</ToggleButton>
				<ToggleButton
					value="Wrong sources" aria-label='Wrong sources'
					className={classNames(
						'checkbox-button',
						{'selected': checkboxValues.includes('Wrong sources')}
					)}>
					{t('feedback.checkboxes.wrongSources')}
				</ToggleButton>
				<ToggleButton
					value="Other" aria-label='Other'
					className={classNames(
						'checkbox-button',
						{'selected': checkboxValues.includes('Other')}
					)}>
					{t('feedback.checkboxes.other')}
				</ToggleButton>
			</ToggleButtonGroup>

			<TextField placeholder={t('feedback.placeholders.moreDetails')} multiline fullWidth rows={2} value={description} onChange={handleDescrptionChange} />

			<TextField placeholder={t('feedback.placeholders.email')} size='small' fullWidth variant="outlined" style={{ width: '100%' }} value={email} onChange={handleEmailChange} />

			<NeButton onClick={handleSendClick} disabled={isFormEmpty} className="query-button">
				{t('feedback.buttons.submit')}
			</NeButton>
		</div>
	);
};

WhatsWrong.propTypes = {
	showFeedback: PropTypes.bool.isRequired,
	messageId: PropTypes.number.isRequired,
	handleFeedbackClick: PropTypes.func.isRequired,
};

export default WhatsWrong;
