import React, { useContext } from 'react';
import { ChatContext } from '../../../contexts';
import PropTypes from 'prop-types';

import { InputAdornment } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { Button as NeButton } from '@nintexglobal/earthling-react';

const SendButton = ({ isDisabled, sendQuery }) => {
	const { isWaiting } = useContext(ChatContext);

	return (
		<InputAdornment position="end">
			<NeButton
				showSpinner={isWaiting}
				onClick={sendQuery}
				disabled={isDisabled}
				className="query-button"
			> 
				{!isWaiting && <SendIcon />}
			</NeButton>
		</InputAdornment>
	);
};

SendButton.propTypes = {
	isDisabled: PropTypes.bool,
	sendQuery: PropTypes.func,
};

export default SendButton;