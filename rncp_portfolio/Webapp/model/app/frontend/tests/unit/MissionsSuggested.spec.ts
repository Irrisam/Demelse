import { render, screen } from '@testing-library/vue'
import Missions from '@/pages/pros/missions_suggested.vue'

test('affiche les missions suggérées', async () => {
    render(Missions)
    const elements = await screen.findAllByText(/Missions suggérées/i)
    expect(elements.length).toBeGreaterThan(0)
})
