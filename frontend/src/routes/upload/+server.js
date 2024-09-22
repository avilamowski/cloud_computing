import { json } from '@sveltejs/kit';
import * as api from '$lib/api';

export async function POST({ request }) {
    try {
        const formData = await request.formData();
        const file = formData.get('image');
        
        if (!file) {
            return json({ error: 'No image file uploaded' }, { status: 400 });
        }

        const buffer = await file.arrayBuffer();
        const base64Image = Buffer.from(buffer).toString('base64');

        // get file extension
        const extension = file.name.split('.').pop();

        const response = await api.post(`upload_image`,
            {
                    image_data: base64Image,
                    file_type: extension
            },
        );

        return json(response, { status: 200 });

    } catch (error) {
        console.error('Error uploading image:', error);
        return json({ error: 'An error occurred during image upload' }, { status: 500 });
    }
}