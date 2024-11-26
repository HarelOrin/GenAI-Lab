import React from 'react';
import { useTranslation } from 'react-i18next';

import PropTypes from 'prop-types';
import classNames from 'classnames';

import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import ThumbDownOffAltOutlinedIcon from '@mui/icons-material/ThumbDownOffAltOutlined';
import { ToggleButton, ToggleButtonGroup } from '@mui/material';

import './ToggleButtons.css';

const ToggleButtons = ({state, showText, hide, handleChange}) => {
	ToggleButtons.propTypes = {
		state: PropTypes.string,
		showText: PropTypes.bool.isRequired,
		hide: PropTypes.bool.isRequired,
		handleChange: PropTypes.func.isRequired
	};

	const { t } = useTranslation();

	return (
		<ToggleButtonGroup
			value={state}
			exclusive
			onChange={handleChange}
			aria-label="text alignment"
		>
			<ToggleButton value="like" aria-label="like" className={classNames(
				'custom-toggle-button',
				{'icon-only': hide},
				{'selected': state === 'like'}
			)}>
				<ThumbUpOutlinedIcon sx={{ fontSize: '16px', padding: 'auto' }}/>
				{showText && (<span className='button-text'>
					{t('feedback.buttons.yes')}
				</span>)}
			</ToggleButton>
			<ToggleButton value="dislike" aria-label="dislike" className={classNames(
				'custom-toggle-button',
				{'icon-only': hide},
				{'selected': state === 'dislike'}
			)}>
				<ThumbDownOffAltOutlinedIcon  sx={{ fontSize: '16px', padding: 'auto' }}/>
				{showText && (<span className='button-text'>
					{t('feedback.buttons.no')}
				</span>)}
			</ToggleButton>
		</ToggleButtonGroup>
	);
};

export default ToggleButtons;