// import React, { useContext, useState } from 'react';
// import { ChatContext } from '../../contexts/chatContext';
// import { ProductContext } from '../../contexts/ProductContext';
// import { ThemeContext } from '../../contexts/ThemeContext';

// import { ThemeProvider } from '@mui/material/styles';
// import { Button, Menu, MenuItem, ListItemIcon} from '@mui/material';

// import { Icon as NeIcon } from '@nintexglobal/earthling-react';

// const ChangeProduct = () => {
// 	// Product & Session management
// 	const { theme } = useContext(ThemeContext);
// 	const { product, setProduct, productData } = useContext(ProductContext);
// 	const { resetSession, sessionID } = useContext(ChatContext);
// 	const [anchorEl, setAnchorEl] = useState(null);

// 	// Functions
// 	const handleClick = (event) => {
// 		setAnchorEl(event.currentTarget);
// 	};

// 	const handleClose = () => {
// 		resetSession(sessionID.current);
// 		setAnchorEl(null);
// 	};


// 	//====================================================================================================
// 	//                                             <ChangeProduct />
// 	//====================================================================================================
// 	return (
// 		<div style={{ fontSize: '14px', width: '100%', display: 'flex', justifyContent: 'flex-end'}}>
// 			<ThemeProvider theme={theme}>
// 				<Button
// 					sx={{ width: '238px', justifyContent: 'flex-start', height: '35px' }}
// 					variant="contained"
// 					onClick={handleClick}
// 					startIcon={
// 						// eslint-disable-next-line
// 						<img src={process.env.PUBLIC_URL + `/assets/productImg/${product.image}`} alt='Not Loaded' style={{ height: '16px' }} />
// 					}
// 				>
// 					<p style={{fontSize: '14px', color: '#A7ABAF'}}>{product.name} </p>
// 					<NeIcon type='caretDown' fixedSize='16px' style={{ marginLeft: 'auto' }} />
// 				</Button>
// 			</ThemeProvider>
// 			<Menu
// 				id="product-menu"
// 				anchorEl={anchorEl}
// 				keepMounted
// 				open={Boolean(anchorEl)}
// 				onClose={handleClose}
// 			>
// 				{productData.map((productItem) => (
// 					productItem.name !== product.name && (
// 						<MenuItem key={productItem.name} onClick={() => {
// 							setProduct(productItem); 
// 							handleClose();
// 						}}>
// 							<ListItemIcon>
// 								{/* eslint-disable-next-line */}
// 								<img src={process.env.PUBLIC_URL + `/assets/productImg/${productItem.image}`} alt='Not Loaded' style={{ height: '14px' }} />
// 							</ListItemIcon>
// 							<p style={{fontSize: '14px'}}>{productItem.name}</p>
// 						</MenuItem>
// 					)
// 				))}
// 			</Menu>
// 		</div>
// 	);
// };

// export default ChangeProduct;
